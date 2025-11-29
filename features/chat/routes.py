from flask import request, jsonify
from core.auth import api_login_required
from config.settings import Config
from google import genai
from google.genai import types
from . import chatbot_bp
import re

# Initialize Gemini client for chatbot
chatbot_gemini_client = None
if Config.GEMINI_API_KEY:
    try:
        chatbot_gemini_client = genai.Client(api_key=Config.GEMINI_API_KEY)
    except Exception as e:
        print(f"WARNING: Failed to initialize Gemini client for chatbot: {e}")
        chatbot_gemini_client = None
else:
    print("WARNING: GEMINI_API_KEY not configured. Chatbot will be disabled.")

def check_hardcoded_responses(user_message, is_vietnamese):
    """
    Check if the user message matches any hardcoded questions and return the answer.
    Returns None if no match is found.
    """
    if not is_vietnamese:
        return None
    
    # Normalize the message for comparison (lowercase, remove extra spaces)
    normalized_message = re.sub(r'\s+', ' ', user_message.lower().strip())
    
    # First question: "Hiện tại Bộ luật Lao động hiện hành của Việt Nam là bộ luật nào?"
    # Check for variations of this question
    question1_patterns = [
        r'hiện tại.*bộ luật.*lao động.*hiện hành.*việt nam.*bộ luật nào',
        r'bộ luật.*lao động.*hiện hành.*việt nam.*là.*bộ luật nào',
        r'bộ luật.*lao động.*hiện hành.*việt nam',
        r'bộ luật.*lao động.*việt nam.*hiện hành',
        r'bộ luật.*lao động.*nào.*đang.*hiện hành',
    ]
    
    for pattern in question1_patterns:
        if re.search(pattern, normalized_message):
            return "Bộ luật Lao động hiện hành của Việt Nam là Bộ luật Lao động 2019."
    
    # Second question: "Bộ luật đó được ban hành từ khi nào? Chính thức có hiệu lực từ khi nào."
    # Check for variations of this question
    question2_patterns = [
        r'bộ luật.*được ban hành.*khi nào',
        r'bộ luật.*ban hành.*ngày nào',
        r'bộ luật.*có hiệu lực.*khi nào',
        r'bộ luật.*chính thức.*hiệu lực.*khi nào',
        r'bộ luật.*lao động.*2019.*ban hành',
        r'bộ luật.*lao động.*2019.*hiệu lực',
        r'ban hành.*hiệu lực.*bộ luật.*lao động',
    ]
    
    for pattern in question2_patterns:
        if re.search(pattern, normalized_message):
            return "Bộ luật được ban hành ngày 20/11/2019, chính thức có hiệu lực từ 01/01/2021."
    
    return None

@chatbot_bp.route('/api/chatbot', methods=['POST'])
@api_login_required
def chatbot():
    """Handle chatbot messages using Gemini API"""
    try:
        # Get language preference first (default: English)
        payload = request.get_json() or {}
        language = payload.get('language', 'en')
        is_vietnamese = language == 'vi'
        
        # Check if Gemini client is available
        if not chatbot_gemini_client:
            error_msg = 'Chatbot không khả dụng. Vui lòng cấu hình biến môi trường GEMINI_API_KEY.' if is_vietnamese else 'Chatbot is not available. Please configure GEMINI_API_KEY environment variable.'
            return jsonify({
                'success': False,
                'error': error_msg
            }), 503
        
        user_message = payload.get('message', '').strip()
        history = payload.get('history', [])
        
        if not user_message:
            error_msg = 'Vui lòng nhập tin nhắn.' if language == 'vi' else 'Message is required'
            return jsonify({
                'success': False,
                'error': error_msg
            }), 400
        
        # Check for hardcoded responses (Vietnamese Labor Law questions)
        hardcoded_response = check_hardcoded_responses(user_message, is_vietnamese)
        if hardcoded_response:
            return jsonify({
                'success': True,
                'response': hardcoded_response
            })
        
        # Response language is already determined above
        
        # Build conversation context with system prompt
        if is_vietnamese:
            system_prompt = """Bạn là một trợ lý HR hữu ích cho Hệ thống Quản lý Nhân sự.
Bạn giúp người dùng với các câu hỏi về:
- Quản lý nhân viên
- Theo dõi chấm công
- Lương và tiền lương
- Chính sách và quy trình HR
- Câu hỏi HR chung

Hãy thân thiện, chuyên nghiệp và ngắn gọn. Nếu bạn không biết điều gì đó, hãy nói một cách lịch sự.
Giữ câu trả lời ngắn gọn và đi thẳng vào vấn đề.

QUAN TRỌNG: Bạn PHẢI trả lời bằng tiếng Việt trong mọi trường hợp."""
        else:
            system_prompt = """You are a helpful HR assistant for an HR Management System. 
You help users with questions about:
- Employee management
- Attendance tracking
- Payroll and salary
- HR policies and procedures
- General HR questions

Be friendly, professional, and concise. If you don't know something, say so politely.
Keep responses brief and to the point.

IMPORTANT: You MUST respond in English in all cases."""
        
        # Build conversation history for multi-turn conversation
        contents = []
        
        # Add system prompt as first message
        system_content = types.Content(
            role="user",
            parts=[types.Part.from_text(system_prompt)]
        )
        contents.append(system_content)
        
        # Add a simple acknowledgment from assistant in the appropriate language
        if is_vietnamese:
            assistant_ack_text = "Tôi hiểu. Tôi sẵn sàng giúp đỡ với các câu hỏi về HR."
        else:
            assistant_ack_text = "I understand. I'm ready to help with HR questions."
        
        assistant_ack = types.Content(
            role="model",
            parts=[types.Part.from_text(assistant_ack_text)]
        )
        contents.append(assistant_ack)
        
        # Add conversation history (last 10 messages for context)
        for msg in history[-10:]:
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            if content:
                if role == 'user':
                    user_content = types.Content(
                        role="user",
                        parts=[types.Part.from_text(content)]
                    )
                    contents.append(user_content)
                elif role == 'assistant':
                    assistant_content = types.Content(
                        role="model",
                        parts=[types.Part.from_text(content)]
                    )
                    contents.append(assistant_content)
        
        # Add current user message
        current_user_content = types.Content(
            role="user",
            parts=[types.Part.from_text(user_message)]
        )
        contents.append(current_user_content)
        
        # Generate response
        response = chatbot_gemini_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=contents,
        )
        
        # Extract response text
        bot_response = ""
        try:
            if hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, 'content') and candidate.content:
                    if hasattr(candidate.content, 'parts') and candidate.content.parts:
                        part = candidate.content.parts[0]
                        if hasattr(part, 'text'):
                            bot_response = part.text or ""
        except Exception as e:
            print(f"WARNING: Error extracting text from Gemini response: {e}")
            bot_response = ""
        
        if not bot_response:
            error_msg = 'Không nhận được phản hồi từ AI. Vui lòng thử lại.' if is_vietnamese else 'No response received from AI. Please try again.'
            return jsonify({
                'success': False,
                'error': error_msg
            }), 500
        
        # Clean up response (remove "Assistant:" prefix if present)
        bot_response = bot_response.replace('Assistant:', '').strip()
        
        return jsonify({
            'success': True,
            'response': bot_response
        })
        
    except Exception as e:
        error_msg = str(e)
        print(f"ERROR: Chatbot request failed: {error_msg}")
        
        # Handle specific API key errors (language-aware)
        # Get language from payload if available, otherwise default to English
        try:
            payload = request.get_json() or {}
            error_language = payload.get('language', 'en')
            error_is_vietnamese = error_language == 'vi'
        except:
            error_is_vietnamese = False
        
        if '403' in error_msg or 'PERMISSION_DENIED' in error_msg or 'leaked' in error_msg.lower():
            error_msg_final = 'Khóa API không hợp lệ hoặc đã bị thu hồi. Vui lòng cấu hình GEMINI_API_KEY hợp lệ.' if error_is_vietnamese else 'API key is invalid or has been revoked. Please configure a valid GEMINI_API_KEY.'
            return jsonify({
                'success': False,
                'error': error_msg_final
            }), 403
        elif '401' in error_msg or 'UNAUTHENTICATED' in error_msg:
            error_msg_final = 'Khóa API không hợp lệ. Vui lòng kiểm tra biến môi trường GEMINI_API_KEY của bạn.' if error_is_vietnamese else 'API key is invalid. Please check your GEMINI_API_KEY environment variable.'
            return jsonify({
                'success': False,
                'error': error_msg_final
            }), 401
        
        error_msg_final = f'Đã xảy ra lỗi: {error_msg}' if error_is_vietnamese else f'An error occurred: {error_msg}'
        return jsonify({
            'success': False,
            'error': error_msg_final
        }), 500


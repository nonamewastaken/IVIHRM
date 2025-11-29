// Shared translations for registration steps
const translations = {
    en: {
        ui: {
            navbar: {
                home: 'Home',
                personnel: 'Administrative Personnel',
                attendance: 'Attendance',
                salary: 'Salary',
                decision: 'Decision',
                evaluateCV: 'Evaluate CV'
            },
            sidebar: {
                home: {
                    title: 'Dashboard Management',
                    overview: 'Dashboard Overview',
                    today: 'Today\'s Summary',
                    notifications: 'Notifications',
                    quickAdd: 'Quick Add',
                    search: 'Search',
                    settings: 'Settings'
                },
                personnel: {
                    title: 'Personnel Management',
                    sections: {
                        overview: 'Overview',
                        employeeManagement: 'Employee Management',
                        departmentManagement: 'Department Management',
                        reports: 'Reports'
                    },
                    overview: 'Overview',
                    cvCustomization: 'CV Customization',
                    addEmployee: 'Add Employee',
                    editEmployee: 'Edit Employee',
                    allEmployees: 'All Employees',
                    addMode: {
                        oneEmployee: 'One Employee',
                        oneEmployeeDesc: 'Create a record for a single employee using the step-by-step wizard.',
                        multipleEmployees: 'Multiple Employees',
                        multipleEmployeesDesc: 'Start a batch onboarding flow. For now, this opens the same wizard and will expand later.',
                        continue: 'Continue'
                    },
                    addEmployeeForm: {
                        stepUploadCV: 'Upload CV',
                        stepPersonalInfo: 'Personal Info',
                        uploadCVTitle: 'Upload CV (Image or PDF)',
                        uploadCVDesc: 'You can upload a CV file (image or PDF) or skip this step — Max 10 files, 100MB each',
                        upload: 'Upload',
                        cvUploaded: 'CV Uploaded',
                        remove: 'Remove',
                        evaluateCV: 'Evaluate CV for Development',
                        cvEvaluationResults: 'CV Evaluation Results',
                        back: 'Back',
                        reset: 'Reset',
                        continue: 'Continue',
                        personalInformation: 'Personal Information',
                        cvParsedSuccess: 'CV parsed. Fields were prefilled when available.',
                        cvNoDataFound: 'CV was read but no extractable information was found. Please fill the form manually.',
                        cvExtractError: 'Could not extract info from the CV.',
                        cvReadError: 'Error reading CV:',
                        readingCV: 'Reading CV to prefill your info...',
                        form: {
                            personalInformation: 'PERSONAL INFORMATION',
                            portraitPhoto: 'Portrait Photo',
                            fullName: 'Full Name',
                            fullNamePlaceholder: 'Full name',
                            gender: 'Gender',
                            male: 'Male',
                            female: 'Female',
                            dateOfBirth: 'Date of Birth',
                            placeOfBirth: 'Place of Birth',
                            placeOfBirthPlaceholder: 'Enter place of birth',
                            hometown: 'Hometown',
                            hometownPlaceholder: 'Enter hometown',
                            maritalStatus: 'Marital Status',
                            single: 'Single',
                            married: 'Married',
                            other: 'Other',
                            ethnicity: 'Ethnicity',
                            ethnicityPlaceholder: 'Enter ethnicity',
                            religion: 'Religion',
                            religionPlaceholder: 'Enter religion',
                            personalTaxCode: 'Personal Tax Code',
                            personalTaxCodePlaceholder: 'Enter personal tax code',
                            socialInsuranceCode: 'Social Insurance Code',
                            socialInsuranceCodePlaceholder: 'Enter social insurance code',
                            personalPhoneNumber: 'Personal Phone Number',
                            personalPhoneNumberPlaceholder: 'Enter personal phone number',
                            personalEmail: 'Personal Email',
                            personalEmailPlaceholder: 'Enter personal email',
                            partyJoinDate: 'Party Join Date',
                            partyJoinPlace: 'Party Join Place',
                            partyJoinPlacePlaceholder: 'Enter party join place',
                            healthStatus: 'Health Status',
                            selectHealthStatus: 'Select health status',
                            healthStatusExcellent: 'Excellent',
                            healthStatusGood: 'Good',
                            healthStatusFair: 'Fair',
                            healthStatusPoor: 'Poor',
                            healthCertificate: 'Health Certificate',
                            emergencyContact: 'Emergency Contact (name + phone)',
                            emergencyContactPlaceholder: 'Name and phone number for emergency contact',
                            permanentResidence: 'PERMANENT RESIDENCE & CURRENT ADDRESS',
                            permanentResidenceLabel: 'Permanent residence e.g., "144 Nghia Do Ward, Hanoi City"',
                            permanentResidencePlaceholder: 'Enter permanent address',
                            currentAddressLabel: 'Current address e.g., "144 Nghia Do Ward, Hanoi City"',
                            currentAddressPlaceholder: 'Enter current address',
                            provinceCity: 'Province/City',
                            selectProvinceCity: 'Select Province/City',
                            wardDistrictTown: 'Ward/District/Town',
                            selectWardDistrictTown: 'Select Ward/District/Town',
                            houseNumberStreet: 'House number, street/hamlet',
                            houseNumberStreetPlaceholder: 'Enter house number, street/hamlet',
                            idCardPassport: 'ID CARD & PASSPORT',
                            idCardNumber: 'ID Card Number',
                            idCardNumberPlaceholder: 'Enter ID card number',
                            passportNumber: 'Passport Number',
                            passportNumberPlaceholder: 'Enter passport number',
                            issueDate: 'Issue Date',
                            expiryDate: 'Expiry Date',
                            idCardIssuePlace: 'Issue Place',
                            idCardIssuePlacePlaceholder: 'Enter ID card issue place',
                            passportIssuePlace: 'Issue Place',
                            passportIssuePlacePlaceholder: 'Enter passport issue place',
                            attachBothSides: 'Attach (both sides)',
                            accountInformation: 'ACCOUNT INFORMATION',
                            employeeEmail: 'Employee Email',
                            employeeEmailPlaceholder: 'Enter email for employee account (optional)',
                            employeeEmailHelp: 'Leave blank if you don\'t want to create a login account for this employee',
                            password: 'Password',
                            passwordPlaceholder: 'Enter password (required if email provided)',
                            generateStrongPassword: 'Generate Strong Password',
                            passwordHelp: 'Password is required if email is provided',
                            passwordStrength: 'Password Strength:',
                            finish: 'Finish',
                            validationFillAll: 'Please fill in all required fields:',
                            errorFullName: 'Please enter full name',
                            errorGender: 'Please select gender',
                            errorDateOfBirth: 'Please enter date of birth',
                            errorPlaceOfBirth: 'Please enter place of birth',
                            errorHometown: 'Please enter hometown',
                            errorPersonalPhone: 'Please enter personal phone number',
                            errorPersonalEmail: 'Please enter personal email',
                            errorIdCardNumber: 'Please enter ID card number',
                            errorIdCardIssueDate: 'Please enter ID card issue date',
                            errorIdCardIssuePlace: 'Please enter ID card issue place'
                        }
                    },
                    companies: 'Companies',
                    divisions: 'Divisions',
                    departments: 'Departments',
                    subDepartments: 'Sub-departments',
                    orgChart: 'Organizational Chart',
                    roles: 'Roles & Positions',
                    reports: 'Personnel Reports',
                    analytics: 'Analytics'
                },
                attendance: {
                    title: 'Attendance Management',
                    overview: 'Overview',
                    monthlyDetail: 'Monthly Attendance Detail',
                    summary: 'Attendance Summary',
                    workData: 'Work Data',
                    history: 'Attendance History',
                    checkInOut: 'Check In/Out',
                    timeClock: 'Time Clock',
                    mobileApp: 'Mobile App',
                    export: 'Export Data',
                    analytics: 'Attendance Analytics',
                    weekly: 'Weekly Reports'
                },
                salary: {
                    title: 'Salary Management',
                    overview: 'Overview',
                    calculate: 'Calculate Salary',
                    payrollList: 'Payroll List',
                    basic: 'Basic Salary',
                    allowances: 'Allowances',
                    deductions: 'Deductions',
                    bonuses: 'Bonuses',
                    slips: 'Salary Slips',
                    reports: 'Salary Reports',
                    print: 'Print Documents'
                },
                decision: {
                    title: 'Decision Management',
                    newDecision: 'New Decision',
                    allDecisions: 'All Decisions',
                    editDecision: 'Edit Decision',
                    approveDecision: 'Approve Decision',
                    hiring: 'Hiring Decisions',
                    termination: 'Termination Decisions',
                    promotion: 'Promotion Decisions',
                    transfer: 'Transfer Decisions',
                    search: 'Search Decisions',
                    history: 'Decision History',
                    analytics: 'Decision Analytics'
                },
                chatbot: {
                    title: 'HR Assistant',
                    welcome: 'Hi there! Please let me know if you have any questions.',
                    placeholder: 'Type here and press Enter to chat',
                    error: 'Sorry, I encountered an error. Please try again.',
                    noResponse: 'No response received. Please try again.'
                }
            }
        },
        // Complete Profile Step
        completeProfile: {
            title: 'Welcome, {name}!',
            subtitle: 'We just need a few details to complete your profile',
            citizenship: 'Citizenship',
            citizenshipPlaceholder: 'Start typing your citizenship',
            dateOfBirth: 'Date of birth',
            dateOfBirthPlaceholder: 'Select your date of birth',
            phoneNumber: 'Phone number',
            phoneNumberPlaceholder: 'Enter your phone number',
            continue: 'Continue',
            nextStep: 'Next step: Your organization',
            errorCitizenship: 'Please select your citizenship',
            errorDate: 'Please enter your date of birth',
            errorPhone: 'Please enter a valid 9-digit phone number'
        },
        // Organization Setup Step
        organizationSetup: {
            title: 'Set up your organization',
            subtitle: 'Tell us about your organization',
            orgName: 'Organization Name',
            orgNamePlaceholder: 'Enter your organization name',
            location: 'Headquarters Location',
            locationPlaceholder: 'Start typing your location',
            back: 'Back',
            continue: 'Continue',
            nextStep: 'Next step: People',
            errorOrgName: 'Please enter organization name',
            errorLocation: 'Please select headquarters location'
        },
        // People Count Step
        peopleCount: {
            title: 'How many people work at your organization?',
            subtitle: 'This helps us customize your experience',
            back: 'Back',
            finishSetup: 'Finish setup',
            errorSize: 'Please select number of employees'
        }
    },
    vi: {
        ui: {
            navbar: {
                home: 'Trang chủ',
                personnel: 'Hành chính nhân sự',
                attendance: 'Chấm công',
                salary: 'Tiền lương',
                decision: 'Quyết định',
                evaluateCV: 'Đánh giá CV'
            },
            sidebar: {
                home: {
                    title: 'Quản lý bảng điều khiển',
                    overview: 'Tổng quan bảng điều khiển',
                    today: 'Tổng kết hôm nay',
                    notifications: 'Thông báo',
                    quickAdd: 'Thêm nhanh',
                    search: 'Tìm kiếm',
                    settings: 'Cài đặt'
                },
                personnel: {
                    title: 'Hành chính nhân sự',
                    sections: {
                        overview: 'Tổng quan',
                        employeeManagement: 'Quản lý nhân viên',
                        departmentManagement: 'Quản lý phòng ban',
                        reports: 'Báo cáo'
                    },
                    overview: 'Tổng quan',
                    cvCustomization: 'Tùy chỉnh CV',
                    addEmployee: 'Thêm nhân viên',
                    editEmployee: 'Chỉnh sửa nhân viên',
                    allEmployees: 'Tất cả nhân viên',
                    addMode: {
                        oneEmployee: 'Một nhân viên',
                        oneEmployeeDesc: 'Tạo hồ sơ cho một nhân viên bằng trình hướng dẫn từng bước.',
                        multipleEmployees: 'Nhiều nhân viên',
                        multipleEmployeesDesc: 'Bắt đầu quy trình tuyển dụng hàng loạt. Hiện tại, điều này sẽ mở cùng một trình hướng dẫn và sẽ được mở rộng sau.',
                        continue: 'Tiếp tục'
                    },
                    addEmployeeForm: {
                        stepUploadCV: 'Tải lên CV',
                        stepPersonalInfo: 'Thông tin cá nhân',
                        uploadCVTitle: 'Tải lên CV (Hình ảnh hoặc PDF)',
                        uploadCVDesc: 'Bạn có thể tải lên tệp CV (hình ảnh hoặc PDF) hoặc bỏ qua bước này — Tối đa 10 tệp, mỗi tệp 100MB',
                        upload: 'Tải lên',
                        cvUploaded: 'CV đã tải lên',
                        remove: 'Xóa',
                        evaluateCV: 'Đánh giá CV để phát triển',
                        cvEvaluationResults: 'Kết quả đánh giá CV',
                        back: 'Quay lại',
                        reset: 'Đặt lại',
                        continue: 'Tiếp tục',
                        personalInformation: 'Thông tin cá nhân',
                        cvParsedSuccess: 'CV đã được phân tích. Các trường đã được điền sẵn khi có sẵn.',
                        cvNoDataFound: 'CV đã được đọc nhưng không tìm thấy thông tin có thể trích xuất. Vui lòng điền biểu mẫu thủ công.',
                        cvExtractError: 'Không thể trích xuất thông tin từ CV.',
                        cvReadError: 'Lỗi đọc CV:',
                        readingCV: 'Đang đọc CV để điền sẵn thông tin của bạn...',
                        form: {
                            personalInformation: 'THÔNG TIN CÁ NHÂN',
                            portraitPhoto: 'Ảnh chân dung',
                            fullName: 'Họ và tên',
                            fullNamePlaceholder: 'Họ và tên',
                            gender: 'Giới tính',
                            male: 'Nam',
                            female: 'Nữ',
                            dateOfBirth: 'Ngày sinh',
                            placeOfBirth: 'Nơi sinh',
                            placeOfBirthPlaceholder: 'Nhập nơi sinh',
                            hometown: 'Quê quán',
                            hometownPlaceholder: 'Nhập quê quán',
                            maritalStatus: 'Tình trạng hôn nhân',
                            single: 'Độc thân',
                            married: 'Đã kết hôn',
                            other: 'Khác',
                            ethnicity: 'Dân tộc',
                            ethnicityPlaceholder: 'Nhập dân tộc',
                            religion: 'Tôn giáo',
                            religionPlaceholder: 'Nhập tôn giáo',
                            personalTaxCode: 'Mã số thuế cá nhân',
                            personalTaxCodePlaceholder: 'Nhập mã số thuế cá nhân',
                            socialInsuranceCode: 'Mã số bảo hiểm xã hội',
                            socialInsuranceCodePlaceholder: 'Nhập mã số bảo hiểm xã hội',
                            personalPhoneNumber: 'Số điện thoại cá nhân',
                            personalPhoneNumberPlaceholder: 'Nhập số điện thoại cá nhân',
                            personalEmail: 'Email cá nhân',
                            personalEmailPlaceholder: 'Nhập email cá nhân',
                            partyJoinDate: 'Ngày vào Đảng',
                            partyJoinPlace: 'Nơi vào Đảng',
                            partyJoinPlacePlaceholder: 'Nhập nơi vào Đảng',
                            healthStatus: 'Tình trạng sức khỏe',
                            selectHealthStatus: 'Chọn tình trạng sức khỏe',
                            healthStatusExcellent: 'Xuất sắc',
                            healthStatusGood: 'Tốt',
                            healthStatusFair: 'Khá',
                            healthStatusPoor: 'Yếu',
                            healthCertificate: 'Giấy khám sức khỏe',
                            emergencyContact: 'Liên hệ khẩn cấp (tên + số điện thoại)',
                            emergencyContactPlaceholder: 'Tên và số điện thoại liên hệ khẩn cấp',
                            permanentResidence: 'NƠI THƯỜNG TRÚ & NƠI Ở HIỆN TẠI',
                            permanentResidenceLabel: 'Nơi thường trú ví dụ: "144 Phường Nghĩa Đô, Thành phố Hà Nội"',
                            permanentResidencePlaceholder: 'Nhập địa chỉ thường trú',
                            currentAddressLabel: 'Nơi ở hiện tại ví dụ: "144 Phường Nghĩa Đô, Thành phố Hà Nội"',
                            currentAddressPlaceholder: 'Nhập địa chỉ hiện tại',
                            provinceCity: 'Tỉnh/Thành phố',
                            selectProvinceCity: 'Chọn Tỉnh/Thành phố',
                            wardDistrictTown: 'Phường/Xã/Thị trấn',
                            selectWardDistrictTown: 'Chọn Phường/Xã/Thị trấn',
                            houseNumberStreet: 'Số nhà, đường/phố',
                            houseNumberStreetPlaceholder: 'Nhập số nhà, đường/phố',
                            idCardPassport: 'CMND/CCCD & HỘ CHIẾU',
                            idCardNumber: 'Số CMND/CCCD',
                            idCardNumberPlaceholder: 'Nhập số CMND/CCCD',
                            passportNumber: 'Số hộ chiếu',
                            passportNumberPlaceholder: 'Nhập số hộ chiếu',
                            issueDate: 'Ngày cấp',
                            expiryDate: 'Ngày hết hạn',
                            idCardIssuePlace: 'Nơi cấp',
                            idCardIssuePlacePlaceholder: 'Nhập nơi cấp CMND/CCCD',
                            passportIssuePlace: 'Nơi cấp',
                            passportIssuePlacePlaceholder: 'Nhập nơi cấp hộ chiếu',
                            attachBothSides: 'Đính kèm (cả hai mặt)',
                            accountInformation: 'THÔNG TIN TÀI KHOẢN',
                            employeeEmail: 'Email nhân viên',
                            employeeEmailPlaceholder: 'Nhập email cho tài khoản nhân viên (tùy chọn)',
                            employeeEmailHelp: 'Để trống nếu bạn không muốn tạo tài khoản đăng nhập cho nhân viên này',
                            password: 'Mật khẩu',
                            passwordPlaceholder: 'Nhập mật khẩu (bắt buộc nếu có email)',
                            generateStrongPassword: 'Tạo mật khẩu mạnh',
                            passwordHelp: 'Mật khẩu là bắt buộc nếu có email',
                            passwordStrength: 'Độ mạnh mật khẩu:',
                            finish: 'Hoàn tất',
                            validationFillAll: 'Vui lòng điền vào tất cả các trường bắt buộc:',
                            errorFullName: 'Vui lòng nhập họ và tên',
                            errorGender: 'Vui lòng chọn giới tính',
                            errorDateOfBirth: 'Vui lòng nhập ngày sinh',
                            errorPlaceOfBirth: 'Vui lòng nhập nơi sinh',
                            errorHometown: 'Vui lòng nhập quê quán',
                            errorPersonalPhone: 'Vui lòng nhập số điện thoại cá nhân',
                            errorPersonalEmail: 'Vui lòng nhập email cá nhân',
                            errorIdCardNumber: 'Vui lòng nhập số CMND/CCCD',
                            errorIdCardIssueDate: 'Vui lòng nhập ngày cấp CMND/CCCD',
                            errorIdCardIssuePlace: 'Vui lòng nhập nơi cấp CMND/CCCD'
                        }
                    },
                    companies: 'Công ty',
                    divisions: 'Khối',
                    departments: 'Phòng ban',
                    subDepartments: 'Bộ phận',
                    orgChart: 'Sơ đồ tổ chức',
                    roles: 'Vai trò & Vị trí',
                    reports: 'Báo cáo nhân sự',
                    analytics: 'Phân tích'
                },
                attendance: {
                    title: 'Quản lý chấm công',
                    overview: 'Tổng quan',
                    monthlyDetail: 'Chi tiết chấm công tháng',
                    summary: 'Tổng hợp chấm công',
                    workData: 'Dữ liệu công việc',
                    history: 'Lịch sử chấm công',
                    checkInOut: 'Vào/Ra',
                    timeClock: 'Đồng hồ thời gian',
                    mobileApp: 'Ứng dụng di động',
                    export: 'Xuất dữ liệu',
                    analytics: 'Phân tích chấm công',
                    weekly: 'Báo cáo tuần'
                },
                salary: {
                    title: 'Quản lý lương',
                    overview: 'Tổng quan',
                    calculate: 'Tính lương',
                    payrollList: 'Danh sách bảng lương',
                    basic: 'Lương cơ bản',
                    allowances: 'Phụ cấp',
                    deductions: 'Khấu trừ',
                    bonuses: 'Thưởng',
                    slips: 'Phiếu lương',
                    reports: 'Báo cáo lương',
                    print: 'In ấn'
                },
                decision: {
                    title: 'Quản lý quyết định',
                    newDecision: 'Tạo quyết định',
                    allDecisions: 'Danh sách quyết định',
                    editDecision: 'Chỉnh sửa quyết định',
                    approveDecision: 'Phê duyệt quyết định',
                    hiring: 'Quyết định tuyển dụng',
                    termination: 'Quyết định chấm dứt',
                    promotion: 'Quyết định thăng chức',
                    transfer: 'Quyết định điều chuyển',
                    search: 'Tìm kiếm quyết định',
                    history: 'Lịch sử quyết định',
                    analytics: 'Phân tích quyết định'
                },
                chatbot: {
                    title: 'Trợ lý nhân sự ảo',
                    welcome: 'Xin chào! Vui lòng cho tôi biết nếu bạn có bất kỳ câu hỏi nào.',
                    placeholder: 'Nhập vào đây và nhấn Enter để trò chuyện',
                    error: 'Xin lỗi, tôi gặp lỗi. Vui lòng thử lại.',
                    noResponse: 'Không nhận được phản hồi. Vui lòng thử lại.'
                }
            }
        },
        // Complete Profile Step
        completeProfile: {
            title: 'Chào mừng, {name}!',
            subtitle: 'Chúng tôi cần một vài thông tin để hoàn tất hồ sơ của bạn',
            citizenship: 'Quốc tịch',
            citizenshipPlaceholder: 'Bắt đầu nhập quốc tịch của bạn',
            dateOfBirth: 'Ngày sinh',
            dateOfBirthPlaceholder: 'Chọn ngày sinh của bạn',
            phoneNumber: 'Số điện thoại',
            phoneNumberPlaceholder: 'Nhập số điện thoại của bạn',
            continue: 'Tiếp tục',
            nextStep: 'Bước tiếp theo: Tổ chức của bạn',
            errorCitizenship: 'Vui lòng chọn quốc tịch',
            errorDate: 'Vui lòng nhập ngày sinh',
            errorPhone: 'Vui lòng nhập số điện thoại hợp lệ 9 chữ số'
        },
        // Organization Setup Step
        organizationSetup: {
            title: 'Thiết lập tổ chức của bạn',
            subtitle: 'Cho chúng tôi biết về tổ chức của bạn',
            orgName: 'Tên tổ chức',
            orgNamePlaceholder: 'Nhập tên tổ chức của bạn',
            location: 'Địa điểm trụ sở',
            locationPlaceholder: 'Bắt đầu nhập địa điểm',
            back: 'Quay lại',
            continue: 'Tiếp tục',
            nextStep: 'Bước tiếp theo: Số lượng người',
            errorOrgName: 'Vui lòng nhập tên tổ chức',
            errorLocation: 'Vui lòng chọn địa điểm trụ sở'
        },
        // People Count Step
        peopleCount: {
            title: 'Có bao nhiêu người làm việc tại tổ chức của bạn?',
            subtitle: 'Điều này giúp chúng tôi tùy chỉnh trải nghiệm của bạn',
            back: 'Quay lại',
            finishSetup: 'Hoàn tất thiết lập',
            errorSize: 'Vui lòng chọn số lượng nhân viên'
        }
    }
};

// Lightweight language utilities for global use
(function () {
    const LANGUAGE_STORAGE_KEY = 'language';
    function t(key, fallback) {
        try {
            const lang = getCurrentLanguage();
            const parts = key.split('.');
            let node = translations[lang];
            for (const p of parts) {
                if (!node || !(p in node)) return fallback;
                node = node[p];
            }
            return typeof node === 'string' ? node : fallback;
        } catch (_) {
            return fallback;
        }
    }
    function getCurrentLanguage() {
        try {
            return localStorage.getItem(LANGUAGE_STORAGE_KEY) || 'en';
        } catch (_) {
            return 'en';
        }
    }
    function setLanguage(lang, options) {
        const opts = Object.assign({ emit: true, persist: true, reload: false }, options || {});
        const next = (lang === 'vi' || lang === 'en') ? lang : 'en';
        try {
            if (opts.persist) localStorage.setItem(LANGUAGE_STORAGE_KEY, next);
        } catch (_) {
            // ignore storage errors
        }
        try {
            document.documentElement.setAttribute('lang', next);
        } catch (_) {}
        try {
            window.CURRENT_LANGUAGE = next;
        } catch (_) {}
        if (opts.emit) {
            try {
                window.dispatchEvent(new CustomEvent('languagechange', { detail: { lang: next } }));
            } catch (_) {}
        }
        if (opts.reload) {
            try { window.location.reload(); } catch (_) {}
        }
        return next;
    }
    function applyTranslations(lang) {
        const current = setLanguage(lang || getCurrentLanguage(), { emit: false, persist: true, reload: false });
        // Navbar labels
        const nav = [
            { id: 'navHome', key: 'ui.navbar.home' },
            { id: 'navPersonnel', key: 'ui.navbar.personnel' },
            { id: 'navAttendance', key: 'ui.navbar.attendance' },
            { id: 'navSalary', key: 'ui.navbar.salary' },
            { id: 'navDecision', key: 'ui.navbar.decision' },
            { id: 'navEvaluateCVText', key: 'ui.navbar.evaluateCV' }
        ];
        nav.forEach(item => {
            const el = document.getElementById(item.id);
            if (el) el.textContent = t(item.key, el.textContent);
        });
        // Re-render sidebar and translate entries
        if (typeof window.forceSidebarInit === 'function') {
            window.forceSidebarInit();
        }
        if (typeof window.translateSidebar === 'function') {
            window.translateSidebar();
        }
        // Emit change after applying
        try {
            window.dispatchEvent(new CustomEvent('languagechange', { detail: { lang: current } }));
        } catch (_) {}
    }
    // Expose to global scope
    try {
        window.translations = translations;
        window.t = t;
        window.getCurrentLanguage = getCurrentLanguage;
        window.setLanguage = setLanguage;
        window.applyTranslations = applyTranslations;
        // Ensure document has initial lang attribute
        const initial = getCurrentLanguage();
        window.CURRENT_LANGUAGE = initial;
        document.documentElement.setAttribute('lang', initial);
    } catch (_) {}
})(); 
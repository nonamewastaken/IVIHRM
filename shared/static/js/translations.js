// Shared translations for registration steps
const translations = {
    en: {
        ui: {
            navbar: {
                home: 'Home',
                personnel: 'Administrative Personnel',
                attendance: 'Attendance',
                salary: 'Salary',
                decision: 'Decision'
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
                    overview: 'Overview',
                    cvCustomization: 'CV Customization',
                    addEmployee: 'Add Employee',
                    allEmployees: 'All Employees',
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
                personnel: 'Nhân sự hành chính',
                attendance: 'Chấm công',
                salary: 'Tiền lương',
                decision: 'Quyết định'
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
                    title: 'Quản lý nhân sự',
                    overview: 'Tổng quan',
                    cvCustomization: 'Tùy chỉnh CV',
                    addEmployee: 'Thêm nhân viên',
                    allEmployees: 'Tất cả nhân viên',
                    companies: 'Công ty',
                    divisions: 'Khối',
                    departments: 'Phòng ban',
                    subDepartments: 'Tổ/nhóm',
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
            { id: 'navDecision', key: 'ui.navbar.decision' }
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
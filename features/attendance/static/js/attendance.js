// Attendance Feature JavaScript

class AttendanceManager {
    constructor() {
        this.currentStatus = null;
        this.updateInterval = null;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadAttendanceStatus();
        this.startTimeUpdate();
    }

    setupEventListeners() {
        // Check in button
        const checkInBtn = document.getElementById('checkInBtn');
        if (checkInBtn) {
            checkInBtn.addEventListener('click', () => this.checkIn());
        }

        // Check out button
        const checkOutBtn = document.getElementById('checkOutBtn');
        if (checkOutBtn) {
            checkOutBtn.addEventListener('click', () => this.checkOut());
        }

        // Filter button for history
        const filterBtn = document.querySelector('.btn-filter');
        if (filterBtn) {
            filterBtn.addEventListener('click', () => this.loadAttendanceHistory());
        }
    }

    startTimeUpdate() {
        this.updateTime();
        this.updateInterval = setInterval(() => {
            this.updateTime();
        }, 1000);
    }

    updateTime() {
        const now = new Date();
        const timeString = now.toLocaleTimeString('vi-VN');
        const dateString = now.toLocaleDateString('vi-VN');
        
        const timeElement = document.getElementById('currentTime');
        const dateElement = document.getElementById('currentDate');
        
        if (timeElement) timeElement.textContent = timeString;
        if (dateElement) dateElement.textContent = dateString;
    }

    async loadAttendanceStatus() {
        try {
            const response = await fetch('/api/attendance-status');
            const data = await response.json();
            
            if (data.error) {
                this.showError(data.error);
                return;
            }
            
            this.currentStatus = data;
            this.updateStatusDisplay(data);
        } catch (error) {
            console.error('Error loading attendance status:', error);
            this.showError('Không thể tải trạng thái chấm công');
        }
    }

    updateStatusDisplay(data) {
        const statusIndicator = document.getElementById('statusIndicator');
        const statusText = document.getElementById('statusText');
        const checkInBtn = document.getElementById('checkInBtn');
        const checkOutBtn = document.getElementById('checkOutBtn');
        const attendanceInfo = document.getElementById('attendanceInfo');
        
        if (!statusIndicator || !statusText) return;

        // Reset classes
        statusIndicator.className = 'status-indicator';
        if (checkInBtn) checkInBtn.className = 'btn-attendance btn-check-in';
        if (checkOutBtn) checkOutBtn.className = 'btn-attendance btn-check-out';
        
        switch(data.status) {
            case 'not_checked_in':
                statusIndicator.classList.add('status-not-checked');
                statusText.textContent = 'Chưa chấm công hôm nay';
                if (checkInBtn) checkInBtn.disabled = false;
                if (checkOutBtn) {
                    checkOutBtn.disabled = true;
                    checkOutBtn.classList.add('btn-disabled');
                }
                if (attendanceInfo) attendanceInfo.style.display = 'none';
                break;
                
            case 'checked_in':
                statusIndicator.classList.add('status-checked-in');
                statusText.textContent = 'Đã check in - Sẵn sàng check out';
                if (checkInBtn) {
                    checkInBtn.disabled = true;
                    checkInBtn.classList.add('btn-disabled');
                }
                if (checkOutBtn) checkOutBtn.disabled = false;
                if (attendanceInfo) {
                    attendanceInfo.style.display = 'grid';
                    const checkInTime = document.getElementById('checkInTime');
                    const checkOutTime = document.getElementById('checkOutTime');
                    if (checkInTime) checkInTime.textContent = data.check_in_time;
                    if (checkOutTime) checkOutTime.textContent = '--:--';
                }
                break;
                
            case 'checked_out':
                statusIndicator.classList.add('status-checked-out');
                statusText.textContent = 'Hoàn thành chấm công hôm nay';
                if (checkInBtn) {
                    checkInBtn.disabled = true;
                    checkInBtn.classList.add('btn-disabled');
                }
                if (checkOutBtn) {
                    checkOutBtn.disabled = true;
                    checkOutBtn.classList.add('btn-disabled');
                }
                if (attendanceInfo) {
                    attendanceInfo.style.display = 'grid';
                    const checkInTime = document.getElementById('checkInTime');
                    const checkOutTime = document.getElementById('checkOutTime');
                    if (checkInTime) checkInTime.textContent = data.check_in_time;
                    if (checkOutTime) checkOutTime.textContent = data.check_out_time;
                }
                break;
        }
    }

    async checkIn() {
        this.showLoading(true);
        this.hideMessages();
        
        try {
            const response = await fetch('/api/check-in', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            const data = await response.json();
            this.showLoading(false);
            
            if (data.error) {
                this.showError(data.error);
            } else {
                this.showSuccess(data.message);
                this.loadAttendanceStatus(); // Reload status
            }
        } catch (error) {
            this.showLoading(false);
            console.error('Error checking in:', error);
            this.showError('Lỗi khi check in');
        }
    }

    async checkOut() {
        this.showLoading(true);
        this.hideMessages();
        
        try {
            const response = await fetch('/api/check-out', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            const data = await response.json();
            this.showLoading(false);
            
            if (data.error) {
                this.showError(data.error);
            } else {
                this.showSuccess(data.message);
                this.loadAttendanceStatus(); // Reload status
            }
        } catch (error) {
            this.showLoading(false);
            console.error('Error checking out:', error);
            this.showError('Lỗi khi check out');
        }
    }

    async loadAttendanceHistory() {
        const startDate = document.getElementById('startDate')?.value;
        const endDate = document.getElementById('endDate')?.value;
        
        if (!startDate || !endDate) {
            this.showError('Vui lòng chọn khoảng thời gian');
            return;
        }
        
        this.showLoading(true);
        this.hideError();
        
        try {
            const params = new URLSearchParams({
                start_date: startDate,
                end_date: endDate
            });
            
            const response = await fetch(`/api/attendance-history?${params}`);
            const data = await response.json();
            
            this.showLoading(false);
            
            if (data.error) {
                this.showError(data.error);
            } else {
                this.displayAttendanceHistory(data);
            }
        } catch (error) {
            this.showLoading(false);
            console.error('Error loading attendance history:', error);
            this.showError('Không thể tải lịch sử chấm công');
        }
    }

    displayAttendanceHistory(data) {
        const history = data.history;
        
        if (history.length === 0) {
            document.getElementById('noData').style.display = 'block';
            document.getElementById('tableContainer').style.display = 'none';
            document.getElementById('summaryCards').style.display = 'none';
            return;
        }
        
        // Show table and summary
        document.getElementById('noData').style.display = 'none';
        document.getElementById('tableContainer').style.display = 'block';
        document.getElementById('summaryCards').style.display = 'grid';
        
        // Calculate summary
        this.calculateSummary(history);
        
        // Populate table
        const tbody = document.getElementById('attendanceTableBody');
        if (tbody) {
            tbody.innerHTML = '';
            
            history.forEach(record => {
                const row = document.createElement('tr');
                
                const date = new Date(record.date);
                const dayOfWeek = this.getDayOfWeek(date.getDay());
                
                row.innerHTML = `
                    <td>${this.formatDate(date)}</td>
                    <td>${dayOfWeek}</td>
                    <td>${record.check_in_time || '--:--'}</td>
                    <td>${record.check_out_time || '--:--'}</td>
                    <td>${record.work_hours ? record.work_hours + 'h' : '--'}</td>
                    <td><span class="status-badge status-${record.status}">${this.getStatusText(record.status)}</span></td>
                    <td>${record.notes || ''}</td>
                `;
                
                tbody.appendChild(row);
            });
        }
    }

    calculateSummary(history) {
        let totalDays = history.length;
        let totalHours = 0;
        let presentDays = 0;
        let absentDays = 0;
        
        history.forEach(record => {
            if (record.work_hours) {
                totalHours += record.work_hours;
            }
            
            if (record.status === 'present') {
                presentDays++;
            } else if (record.status === 'absent') {
                absentDays++;
            }
        });
        
        const totalDaysEl = document.getElementById('totalDays');
        const totalHoursEl = document.getElementById('totalHours');
        const presentDaysEl = document.getElementById('presentDays');
        const absentDaysEl = document.getElementById('absentDays');
        
        if (totalDaysEl) totalDaysEl.textContent = totalDays;
        if (totalHoursEl) totalHoursEl.textContent = Math.round(totalHours * 10) / 10 + 'h';
        if (presentDaysEl) presentDaysEl.textContent = presentDays;
        if (absentDaysEl) absentDaysEl.textContent = absentDays;
    }

    // Utility functions
    formatDate(date) {
        return date.toLocaleDateString('vi-VN');
    }

    getDayOfWeek(dayIndex) {
        const days = ['CN', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7'];
        return days[dayIndex];
    }

    getStatusText(status) {
        const statusMap = {
            'present': 'Có mặt',
            'absent': 'Vắng mặt',
            'late': 'Đi muộn',
            'half_day': 'Nửa ngày'
        };
        return statusMap[status] || status;
    }

    showLoading(show) {
        const loadingEl = document.getElementById('loading');
        if (loadingEl) {
            loadingEl.style.display = show ? 'block' : 'none';
        }
    }

    showError(message) {
        const errorDiv = document.getElementById('errorMessage');
        if (errorDiv) {
            errorDiv.textContent = message;
            errorDiv.style.display = 'block';
            setTimeout(() => {
                errorDiv.style.display = 'none';
            }, 5000);
        }
    }

    showSuccess(message) {
        const successDiv = document.getElementById('successMessage');
        if (successDiv) {
            successDiv.textContent = message;
            successDiv.style.display = 'block';
            setTimeout(() => {
                successDiv.style.display = 'none';
            }, 3000);
        }
    }

    hideMessages() {
        const errorDiv = document.getElementById('errorMessage');
        const successDiv = document.getElementById('successMessage');
        if (errorDiv) errorDiv.style.display = 'none';
        if (successDiv) successDiv.style.display = 'none';
    }

    hideError() {
        const errorDiv = document.getElementById('errorMessage');
        if (errorDiv) errorDiv.style.display = 'none';
    }

    setDefaultDateRange() {
        const endDate = new Date();
        const startDate = new Date();
        startDate.setDate(endDate.getDate() - 30);
        
        const endDateInput = document.getElementById('endDate');
        const startDateInput = document.getElementById('startDate');
        
        if (endDateInput) endDateInput.value = endDate.toISOString().split('T')[0];
        if (startDateInput) startDateInput.value = startDate.toISOString().split('T')[0];
    }

    destroy() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
        }
    }
}

// Initialize attendance manager when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.attendanceManager = new AttendanceManager();
    
    // Set default date range for history page
    if (document.getElementById('startDate')) {
        window.attendanceManager.setDefaultDateRange();
        window.attendanceManager.loadAttendanceHistory();
    }
});

// Cleanup on page unload
window.addEventListener('beforeunload', function() {
    if (window.attendanceManager) {
        window.attendanceManager.destroy();
    }
});


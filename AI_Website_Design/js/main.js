// 导航栏滚动效果
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.backgroundColor = 'rgba(255, 255, 255, 0.95)';
    } else {
        navbar.style.backgroundColor = 'rgba(255, 255, 255, 1)';
    }
});

// 订阅表单处理
const subscribeForm = document.querySelector('.subscribe-form');
const emailInput = subscribeForm.querySelector('input[type="email"]');
const subscribeBtn = subscribeForm.querySelector('.subscribe-btn');

subscribeBtn.addEventListener('click', (e) => {
    e.preventDefault();
    const email = emailInput.value.trim();
    
    if (!email) {
        alert('请输入您的邮箱地址');
        return;
    }
    
    if (!isValidEmail(email)) {
        alert('请输入有效的邮箱地址');
        return;
    }
    
    // TODO: 在这里添加实际的订阅处理逻辑
    alert('感谢您的订阅！');
    emailInput.value = '';
});

// 邮箱验证函数
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// 平滑滚动效果
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});

// 搜索功能
const searchBtn = document.querySelector('.search-btn');
const searchInput = document.querySelector('.search-box input');

searchBtn.addEventListener('click', (e) => {
    e.preventDefault();
    const searchTerm = searchInput.value.trim();
    
    if (!searchTerm) {
        alert('请输入搜索关键词');
        return;
    }
    
    // TODO: 在这里添加实际的搜索处理逻辑
    alert(`搜索: ${searchTerm}`);
}); 
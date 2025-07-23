
document.addEventListener('DOMContentLoaded', function() {
    // 场景选择交互
    const moduleCards = document.querySelectorAll('.module-card');
    moduleCards.forEach(card => {
        card.addEventListener('click', function() {
            // 移除所有选中状态
            moduleCards.forEach(c => c.classList.remove('selected'));
            // 添加当前选中状态
            this.classList.add('selected');
            
            const scene = this.dataset.scene;
            loadInterviewScene(scene);
        });
    });

    // 加载面试场景
    function loadInterviewScene(scene) {
        console.log(`加载面试场景: ${scene}`);
        // 这里将实现场景加载逻辑
        // 实际项目中会调用API获取场景数据
    }

    // 评测反馈可视化
    function renderEvaluationReport(data) {
        const ctx = document.getElementById('radarChart').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'radar',
            data: {
                labels: data.indicators.map(item => item.name),
                datasets: [{
                    label: '能力评估',
                    data: data.indicators.map(item => item.score),
                    backgroundColor: 'rgba(52, 152, 219, 0.2)',
                    borderColor: 'rgba(52, 152, 219, 1)',
                    borderWidth: 2,
                    pointBackgroundColor: 'rgba(52, 152, 219, 1)',
                    pointRadius: 4
                }]
            },
            options: {
                scales: {
                    r: {
                        angleLines: {
                            display: true
                        },
                        suggestedMin: 0,
                        suggestedMax: 100,
                        ticks: {
                            stepSize: 20
                        }
                    }
                }
            }
        });

        // 渲染改进建议
        const suggestionList = document.querySelector('.suggestion-list');
        suggestionList.innerHTML = data.suggestions
            .map(suggestion => `<li>${suggestion}</li>`)
            .join('');
    }

    // 模拟获取评测数据
    function fetchEvaluationData() {
        // 实际项目中会调用API获取评测数据
        return {
            indicators: [
                {name: '专业知识', score: 85},
                {name: '技能匹配', score: 78},
                {name: '表达能力', score: 90},
                {name: '逻辑思维', score: 82},
                {name: '创新能力', score: 75}
            ],
            suggestions: [
                "建议使用STAR结构回答问题",
                "注意保持适当的眼神交流",
                "技术细节描述可以更具体"
            ]
        };
    }

    // 学习路径交互
    function setupLearningPath() {
        const pathCards = document.querySelectorAll('.path-card');
        pathCards.forEach(card => {
            card.addEventListener('click', function() {
                // 这里可以添加跳转到具体学习资源的逻辑
                console.log('选择学习路径:', this.querySelector('h3').textContent);
            });
        });
    }

    // 初始化页面
    function init() {
        // 默认加载第一个场景
        if (moduleCards.length > 0) {
            moduleCards[0].click();
        }
        
        // 初始化学习路径交互
        setupLearningPath();
        
        // 加载Chart.js库
        loadChartJS();
    }

    // 动态加载Chart.js
    function loadChartJS() {
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/chart.js';
        script.onload = function() {
            // 模拟获取评测数据并渲染
            const evalData = fetchEvaluationData();
            renderEvaluationReport(evalData);
        };
        document.head.appendChild(script);
    }

    init();
});

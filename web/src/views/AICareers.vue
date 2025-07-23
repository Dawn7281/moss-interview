
<template>
  <div class="ai-careers">
    <h1>人工智能职业方向选择</h1>
    <p>请选择您感兴趣的人工智能职业方向</p>
    
    <div class="career-options">
      <div 
        v-for="career in careers" 
        :key="career.id"
        class="career-card"
      >
        <h3>{{ career.category }}</h3>
        <h4>{{ career.title }}</h4>
        <p>{{ career.skills }}</p>
        <div class="career-actions">
          <button @click.stop="openDetails(career)" class="btn-details">查看详情</button>
          <button @click.stop="selectCareer(career)" class="btn-select">选择面试</button>
        </div>
      </div>

      <div v-if="showDetails" class="career-modal">
        <div class="modal-content">
          <h2>{{ selectedCareer.category }}</h2>
          <h3>{{ selectedCareer.title }}</h3>
          <div class="modal-body">
            <p><strong>所需技能:</strong> {{ selectedCareer.skills }}</p>
            <p><strong>典型工作内容:</strong></p>
            <ul>
              <li v-for="(item, index) in getJobDescription(selectedCareer.id)" :key="index">
                {{ item }}
              </li>
            </ul>
          </div>
          <div class="modal-actions">
            <button @click="showDetails = false" class="btn-close">关闭</button>
            <button @click="selectCareer(selectedCareer)" class="btn-select">选择面试</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'AICareersView',
  setup() {
    const router = useRouter()
    
    const careers = [
      {
        id: 'algorithm',
        category: '算法开发类',
        title: '机器学习/深度学习/NLP/视觉工程师',
        skills: 'Python, TensorFlow, PyTorch, 算法'
      },
      {
        id: 'application',
        category: '应用开发类',
        title: 'AI应用开发, MLOps',
        skills: 'API集成, 云计算, 部署自动化'
      },
      {
        id: 'data',
        category: '数据处理类',
        title: '数据科学家, 数据工程师',
        skills: 'SQL, 数据清洗, 可视化'
      },
      {
        id: 'research',
        category: '研究创新类',
        title: 'AI研究科学家, 算法优化',
        skills: '数学, 论文发表, 算法创新'
      },
      {
        id: 'industry',
        category: '行业应用类',
        title: '智能制造, 智能金融, AI医疗',
        skills: '行业知识 + AI算法'
      }
    ]

    const showDetails = ref(false)
    const selectedCareer = ref(null)

    const openDetails = (career) => {
      selectedCareer.value = career
      showDetails.value = true
    }

    const selectCareer = (career) => {
      console.log('选择了职业:', career.title)
      router.push({
        path: '/interview/ai',
        query: {
          career: career.id,
          title: career.title
        }
      })
    }

    const getJobDescription = (careerId) => {
      const descriptions = {
        algorithm: [
          "开发和优化机器学习算法",
          "实现和调优深度学习模型",
          "解决复杂的技术问题"
        ],
        application: [
          "设计和实现AI应用系统",
          "构建和维护MLOps流程",
          "优化模型部署和推理性能"
        ],
        data: [
          "清洗和预处理大规模数据",
          "设计和实现数据管道",
          "创建数据可视化和报告"
        ],
        research: [
          "研究前沿AI算法和技术",
          "设计和执行实验",
          "撰写学术论文和技术专利"
        ],
        industry: [
          "分析行业特定需求",
          "定制AI解决方案",
          "评估技术商业价值"
        ]
      }
      return descriptions[careerId] || []
    }

    return {
      careers,
      selectCareer,
      showDetails,
      selectedCareer,
      openDetails,
      getJobDescription
    }
  }
}
</script>

<style scoped>
.ai-careers {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
}

.career-options {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

.career-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.career-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.career-card h3 {
  color: #3498db;
  margin-bottom: 0.5rem;
}

.career-card h4 {
  margin: 0.5rem 0;
  color: #2c3e50;
}

.career-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}

.btn-details, .btn-select {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  font-size: 0.9rem;
  cursor: pointer;
}

.btn-details {
  background-color: #3498db;
  color: white;
}

.btn-select {
  background-color: #2ecc71;
  color: white;
}

.career-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  max-width: 600px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
}

.modal-body {
  margin: 1.5rem 0;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.btn-close {
  background-color: #e74c3c;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>

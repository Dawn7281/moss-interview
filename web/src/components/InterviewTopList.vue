<template>
  <div class="top-list-container">
    <div class="top-list-header">
      <h3>面试次数最高榜</h3>
    </div>
    
    <div class="top-list-content">
      <div class="scrollable-content">
        <div 
          v-for="(item, index) in topList" 
          :key="item.id" 
          class="top-list-item"
          :class="getRankClass(index)"
        >
          <div class="rank-number">
            {{ index + 1 }}
            <span class="top-icon" v-if="index === 0">🔥</span>
          </div>
          <div class="item-content">
            <div class="item-title">{{ item.username }} - {{ item.location }} - {{ item.university }}</div>
            <div class="item-meta">
<!--              <span class="heat-value">{{ item.heat }}次</span>-->
              <span class="flame-icon" :class="'flame-' + (index + 1)"></span>
<!--              <span v-if="item.isHot" class="hot-tag">面经分享中</span>-->
              <span class="interview-count" v-if="item.interviewCount">
                <i class="icon-interview"></i>{{ item.interviewCount }}次面试
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {getInterviewTopList} from "@/api/interview";

export default {
  name: 'InterviewTopList',
  data() {
    return {
      topList: []
    }
  },
  methods: {
    getRankClass(index) {
      return {
        'first-rank': index === 0,
        'second-rank': index === 1,
        'third-rank': index === 2,
        'other-rank': index > 2
      }
    }
  },
  mounted() {
    getInterviewTopList().then((res) => {
      console.log(res.data)
      this.topList = res.data
    })
  }
}
</script>

<style lang="scss" scoped>
@import url('https://fonts.googleapis.com/css2?family=Pacifico&display=swap');

.top-list-container {
  width: 29%;
  margin: 10px 0 0 20px;
  padding: 0;
  background: #F8F9FA;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);

  .top-list-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0;
    padding: 15px 20px;
    background: linear-gradient(90deg, #ffedf1 0%, #fff0f1 60%, #f7f0ed 100%);
    border-radius: 8px 8px 0 0;
    
    h3 {
      font-size: 18px;
      font-weight: bold;
      margin: 0;
      color: #000000;
    }
    
    .more-link {
      font-size: 14px;
      color: #6C757D;
      text-decoration: none;
      transition: color 0.2s;
      
      &:hover {
        color: #32ca99;
      }
    }
  }
  
  .top-list-content {
    padding: 0;
    height: 100%;
    
    .scrollable-content {
      height: 100%;
      overflow-y: auto;
      padding: 0 20px;
      
      &::-webkit-scrollbar {
        width: 6px;
      }
      
      &::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 3px;
      }
      
      &::-webkit-scrollbar-thumb {
        background: #c1c1c1;
        border-radius: 3px;
        
        &:hover {
          background: #a8a8a8;
        }
      }
      
      .top-list-item {
        display: flex;
        align-items: flex-start;
        padding: 12px 0;
        border-bottom: 1px solid #f0f0f0;
        
        &:last-child {
          border-bottom: none;
        }
        
        .rank-number {
          position: relative;
          width: 24px;
          height: 24px;
          display: flex;
          z-index: 1;
          align-items: center;
          justify-content: center;
          margin-right: 12px;
          font-family: 'Pacifico', cursive;
          font-weight: normal;
          
          .top-icon {
            position: absolute;
            top: -8px;
            right: -8px;
            
            font-size: 12px;
          }
        }
        
        .item-content {
          flex: 1;
          
          .item-title {
            font-size: 15px;
            color: #333;
            margin-bottom: 8px;
            line-height: 1.4;
            font-weight: 500;
          }
          
          .item-meta {
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 8px;
            
            .heat-value {
              font-size: 13px;
              color: #666;
              font-weight: normal;
            }
            
            .flame-icon {
              display: inline-block;
              width: 16px;
              height: 16px;
              background-size: contain;
              background-repeat: no-repeat;
            }
            
            .hot-tag {
              font-size: 12px;
              color: #e74c3c;
              background: #fdecea;
              padding: 2px 6px;
              border-radius: 3px;
              font-weight: normal;
            }
            
            .interview-count {
              font-size: 12px;
              color: #666;
              display: flex;
              align-items: center;
              
              .icon-interview {
                display: inline-block;
                width: 14px;
                height: 14px;
                margin-right: 4px;
                background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%23666'%3E%3Cpath d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z'/%3E%3C/svg%3E");
                background-size: contain;
              }
            }
          }
        }
      }
      
      .first-rank {
        .rank-number {
          color: #FF0000;
          font-size: 18px;
        }
        
        .flame-icon {
          background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%23FF0000'%3E%3Cpath d='M12 23a7.5 7.5 0 0 1-5.138-12.963C8.204 8.774 11.5 6.5 11 1.5c6 4 9 8 3 14 1 0 2.5 0 5-2.47.27.773.5 1.604.5 2.47A7.5 7.5 0 0 1 12 23z'/%3E%3C/svg%3E");
        }
      }
      
      .second-rank {
        .rank-number {
          color: #FFA500;
          font-size: 18px;
        }
        
        .flame-icon {
          background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%23FFA500'%3E%3Cpath d='M12 23a7.5 7.5 0 0 1-5.138-12.963C8.204 8.774 11.5 6.5 11 1.5c6 4 9 8 3 14 1 0 2.5 0 5-2.47.27.773.5 1.604.5 2.47A7.5 7.5 0 0 1 12 23z'/%3E%3C/svg%3E");
        }
      }
      
      .third-rank {
        .rank-number {
          color: #FFA500;
          font-size: 18px;
        }
        
        .flame-icon {
          background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%23FFA500'%3E%3Cpath d='M12 23a7.5 7.5 0 0 1-5.138-12.963C8.204 8.774 11.5 6.5 11 1.5c6 4 9 8 3 14 1 0 2.5 0 5-2.47.27.773.5 1.604.5 2.47A7.5 7.5 0 0 1 12 23z'/%3E%3C/svg%3E");
        }
      }
      
      .other-rank {
        .rank-number {
          color: #6C757D;
          font-size: 16px;
        }
        
        .flame-icon {
          background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%236C757D'%3E%3Cpath d='M12 23a7.5 7.5 0 0 1-5.138-12.963C8.204 8.774 11.5 6.5 11 1.5c6 4 9 8 3 14 1 0 2.5 0 5-2.47.27.773.5 1.604.5 2.47A7.5 7.5 0 0 1 12 23z'/%3E%3C/svg%3E");
        }
      }
    }
  }
}

@media (max-width: 992px) {
  .top-list-container {
    width: 100%;
    margin: 20px 0 0 0;
  }
}
</style>
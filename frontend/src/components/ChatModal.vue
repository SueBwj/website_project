<template>
  <!-- 聊天模态框 -->
  <div
    class="modal fade"
    id="borderTest"
    tabindex="-1"
    role="dialog"
    :class="{ show: isVisible }"
    :style="{ display: isVisible ? 'block' : 'none' }"
  >
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <!-- 模态框头部 -->
        <div class="modal-header">
          <h5 class="modal-title">{{ mode }}</h5>
          <button type="button" class="close btn" @click="closeModal" aria-label="关闭">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <!-- 模态框主体 -->
        <div class="chat-container">
          <div id="chatContent" ref="chatContent">
            <!-- 聊天内容 -->
            <div
              v-for="(msg, index) in messages"
              :key="index"
              :class="['chat-message', getMessageClass(msg.sender)]"
            >
              <!-- 头像 -->
              <img
                :src="getAvatar(msg.sender)"
                alt="avatar"
                class="avatar"
                @error="handleImageError"
              />
              <!-- 消息内容 -->
              <div class="message-text" v-html="formatMessage(msg.text)">
              </div>
            </div>
          </div>
        </div>
        <!-- 模态框底部 -->
        <div class="modal-footer">
          <input
            type="text"
            class="form-control"
            v-model="message"
            @keyup.enter="sendMessage"
            placeholder="输入消息..."
          />
          <button type="button" class="btn send-button" @click="sendMessage">
            发送
          </button>
        </div>
        <!-- 归属信息 -->
        <div class="attribution">
          Icon by <a href="https://www.flaticon.com/free-icon/ai_2814666?term=robot&page=1&position=9&origin=search&related_id=2814666" target="_blank">Flaticon</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: 'ChatModal',
  props: {
    visible: {
      type: Boolean,
      default: false,
    },
    mode: {
      type: String,
      default: 'Chat'
    },
    claim: {
      type: String
    },
    userAvatar: { // 用户头像
      type: String,
      default: 'https://via.placeholder.com/40?text=U' // 默认用户头像
    },
    botAvatar: { // 机器人头像
      type: String,
      default: 'https://www.flaticon.com/svg/static/icons/svg/2814/2814666.svg' // Flaticon 机器人头像URL
    }
  },
  data() {
    return {
      message: '',
      messages: []
    };
  },
  computed: {
    isVisible() {
      return this.visible;
    },
  },
  watch:{
    claim(newVal){
      console.log("newVal",newVal)
      if(newVal.trim() !== ''){
        // 在开启新话题的时候清空聊天窗口
        this.messages = [{ text: '正在加载回复...', sender: 'bot' }]
        this.getGptReply()
      }
    }
  },
  methods: {
    closeModal() {
      this.$emit('close');
    },
    sendMessage() {
      if (this.message.trim() !== '') {
        const userMessage = this.message;
        this.messages.push({ text: userMessage, sender: 'user' });
        this.message = '';

        // 模拟回复
        setTimeout(() => {
          this.messages.push({ text: '这是自动回复的消息', sender: 'bot' });
          this.scrollToBottom();
        }, 1000);
      }
    },
    getMessageClass(sender) {
      return sender === 'user' ? 'user-message' : 'bot-message';
    },
    getAvatar(sender) {
      return sender === 'user' ? this.userAvatar : this.botAvatar;
    },
    getGptReply(){
      axios.get(`http://localhost:5000/roleplay?claim=${this.claim}`)
      .then(response => {
        this.messages.push({text: response.data, sender: 'bot'})
        this.scrollToBottom();
      })
      .catch(error => {
        console.error('roleplay first reply error', error)
      })
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const chatContent = this.$refs.chatContent;
        if (chatContent) {
          chatContent.scrollTop = chatContent.scrollHeight;
        }
      });
    },
    formatMessage(text) {
      // 转换有序列表
      const listPattern = /^(\d+\.\s.+(\n|$))+/
      if (listPattern.test(text)) {
        const listItems = text.split('\n').filter(item => item.trim() !== '');
        const formattedList = listItems.map(item => `<li>${item.replace(/^\d+\.\s/, '')}</li>`).join('');
        return `<ol>${formattedList}</ol>`;
      }
      // 保留换行
      return text.replace(/\n/g, '<br>');
    },
    handleImageError(event) {
      // 头像加载失败时显示默认占位图
      event.target.src = 'https://via.placeholder.com/40?text=?';
    }
  },
};
</script>

<style scoped>
/* 自定义样式 */

/* 基础模态框样式 */
.modal {
  background: rgba(255, 255, 255, 0.8); /* 浅色背景 */
}

.modal-dialog {
  width: 700px; /* 增加宽度 */
  max-width: 95%;
}

.modal-content {
  background: #f9f9f9; /* 浅色背景 */
  border: none;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

/* 头部样式 */
.modal-header {
  background: #ffffff; /* 统一的浅色调 */
  color: #333;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 15px 20px;
  border-bottom: 1px solid #ddd;
}

.modal-header .modal-title {
  font-family: 'Roboto', sans-serif;
  font-weight: 500;
}

.modal-header .close {
  font-size: 24px;
  color: #bbb;
  transition: color 0.3s;
}

.modal-header .close:hover {
  color: #333;
}

/* 聊天区域样式 */
.chat-container {
  background: #ffffff;
  padding: 20px;
  height: 500px; /* 增加高度 */
  overflow-y: auto;
}

#chatContent {
  display: flex;
  flex-direction: column;
}

/* 聊天气泡样式 */
.chat-message {
  display: flex;
  align-items: flex-start;
  margin: 10px 0;
}

/* 头像样式 */
.chat-message .avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin: 0 10px;
}

/* 消息内容样式 */
.message-text {
  max-width: 70%;
  padding: 12px 18px;
  border-radius: 15px;
  background: #e0e0e0;
  color: #333;
  font-family: 'Roboto', sans-serif;
  word-wrap: break-word;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  position: relative;
  white-space: pre-wrap; /* 保留换行符 */
}

/* 用户消息样式 */
.user-message {
  align-self: flex-end;
  flex-direction: row-reverse; /* 将头像放在右侧 */
}

.user-message .avatar {
  margin: 0 0 0 10px; /* 调整头像间距 */
}

.user-message .message-text {
  background: #198754; /* 统一的主色调 */
  color: #fff;
  border-bottom-right-radius: 0;
}

/* 机器人消息样式 */
.bot-message {
  align-self: flex-start;
  flex-direction: row; /* 将头像放在左侧 */
}

.bot-message .avatar {
  margin: 0 10px 0 0; /* 调整头像间距 */
}

.bot-message .message-text {
  background: #e0e0e0;
  color: #333;
  border-bottom-left-radius: 0;
}

/* 底部样式 */
.modal-footer {
  display: flex;
  padding: 15px 20px;
  background: #ffffff; /* 统一的浅色调 */
  border-top: 1px solid #ddd;
}

.modal-footer input {
  flex: 1;
  padding: 10px 15px;
  border: 1px solid #ccc;
  border-radius: 20px;
  background: #f5f5f5;
  color: #333;
  font-size: 14px;
  outline: none;
  transition: background 0.3s, border-color 0.3s;
}

.modal-footer input::placeholder {
  color: #aaa;
}

.modal-footer input:focus {
  background: #ffffff;
  border-color: #198754;
}

.send-button {
  margin-left: 10px;
  padding: 10px 20px;
  border: none;
  border-radius: 20px;
  background: #198754; /* 统一的主色调 */
  color: #fff;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.3s, transform 0.2s;
}

.send-button:hover {
  background: #15602b; /* 深化颜色以显示悬停效果 */
  transform: translateY(-2px);
}

/* 滚动条样式 */
.chat-container::-webkit-scrollbar {
  width: 8px;
}

.chat-container::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.chat-container::-webkit-scrollbar-thumb {
  background-color: #c1c1c1;
  border-radius: 4px;
}

/* 有序列表样式 */
.message-text ol {
  padding-left: 20px;
}

.message-text li {
  margin-bottom: 5px;
}

/* 响应式调整 */
@media (max-width: 800px) {
  .modal-dialog {
    width: 90%;
  }

  .modal-footer input {
    width: 100%;
  }

  .send-button {
    width: 100%;
    margin-left: 0;
    margin-top: 10px;
  }

  .chat-message {
    flex-direction: column;
    align-items: flex-start;
  }

  .user-message {
    align-self: flex-end;
  }

  .user-message .avatar {
    margin: 10px 0 0 0;
  }

  .message-text {
    max-width: 100%;
  }
}

/* 归属信息样式 */
.attribution {
  text-align: center;
  font-size: 10px;
  color: #aaa;
  padding: 5px 0;
}

.attribution a {
  color: #aaa;
  text-decoration: none;
}

.attribution a:hover {
  color: #4a90e2;
}
</style>

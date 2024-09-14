<template>
    <!-- 聊天模态框 -->
    <div
      class="modal fade"
      tabindex="-1"
      role="dialog"
      :class="{ show: isVisible }"
      :style="{ display: isVisible ? 'block' : 'none' }"
    >
      <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
          <!-- 模态框头部 -->
          <div class="modal-header">
            <h5 class="modal-title">{{ this.mode }}</h5>
            <button type="button" class="close" @click="closeModal" aria-label="关闭">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <!-- 模态框主体 -->
          <div class="modal-body">
            <div id="chatContent" style="height: 300px; overflow-y: auto;">
              <!-- 聊天内容 -->
              <div
                v-for="(msg, index) in messages"
                :key="index"
                :class="getMessageClass(msg.sender)"
              >
                {{ msg.text }}
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
            <button type="button" class="btn btn-primary" @click="sendMessage">
              发送
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
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
      }
    },
    data() {
      return {
        message: '',
        messages: [],
      };
    },
    computed: {
      isVisible() {
        return this.visible;
      },
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
          }, 1000);
        }
      },
      getMessageClass(sender) {
        return sender === 'user'
          ? 'text-right mb-2 bg-success text-white p-2 rounded'
          : 'text-left mb-2 bg-light text-dark p-2 rounded';
      },
    },
  };
  </script>
  
  <style scoped>
  /* 自定义样式 */
  .modal {
    background: rgba(0, 0, 0, 0.5);
  }
  #chatContent div {
    padding: 8px 12px;
    border-radius: 15px;
    max-width: 70%;
  }
  #chatContent .text-right {
    background-color: #dcf8c6;
    margin-left: auto;
  }
  #chatContent .text-left {
    background-color: #f1f0f0;
    margin-right: auto;
  }
  </style>
  
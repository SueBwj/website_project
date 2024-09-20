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
    <div class="modal-dialog modal-dialog-centered" id="borderTest" role="document">
      <div class="modal-content">
        <!-- 模态框头部 -->
        <div class="modal-header" id="headerBackground">
          <h5 class="modal-title">{{ this.mode }}</h5>
          <button type="button" class="close btn btn-outline-light" @click="closeModal" aria-label="关闭">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <!-- 模态框主体 -->
        <div class="chatBackground">
          <div id="chatContent" style="height: 400px; overflow-y: auto;padding: 10px;">
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
        <div class="modal-footer" id="footerBackground">
          <input
            type="text"
            class="form-control"
            v-model="message"
            @keyup.enter="sendMessage"
            placeholder="输入消息..."
          />
          <button type="button" class="btn btn-success" @click="sendMessage">
            发送
          </button>
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
        // 在开启新话题的时候对清空聊天窗口
        this.messages = [{ text: 'loading reply...', sender: 'bot' }]
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
        }, 1000);
      }
    },
    getMessageClass(sender) {
      return sender === 'user'
        ? 'text-right mb-2 text-dark p-2 rounded-1 '
        : 'text-left mb-2 text-dark p-2 rounded-1';
    },
    getGptReply(){
      axios.get(`http://localhost:5001/roleplay?claim=${this.claim}`)
      .then(response => {
        this.messages.push({text: response.data, sender: 'bot'})
      })
      .catch(error => {
        console.error('roleplay first reply error', error)
      })
    }
  },
};
</script>

<style scoped>
/* 自定义样式 */
.modal {
  background: rgba(0, 0, 0, 0.5);
}
.modal-header .close {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 20px; /* 调整关闭按钮的字体大小 */
  padding-top: 0px;
  padding-left: 3px;
  padding-right: 3px;
  padding-bottom: 0px;
}
.modal-footer input {
  margin-left: auto;
  width: 250px;
}
.modal-footer button {
  background-color: rgb(66, 186, 136,0.8);
  border-radius:10%;
  height:35px;
  margin-left: 8px;
  text-align: center;
  font-size: 12px;
}
/* 调节模态框宽度 */
.modal-dialog {
  width: 350px;
}
/* header背景颜色 */
#headerBackground {
  /* background-color:hsla(147, 89%, 36%, 0.324); */
  background-color:rgba(171, 196, 190, 0.422);
}
/* footer背景颜色 */
#footerBackground {
  background-color:rgba(171, 196, 190, 0.422);
}
#chatContent div {
  padding: 8px 12px;
  border-radius: 0;
  max-width:fit-content;
  background-color: rgba(255, 255, 255, 0.8); /* 设置背景颜色为白色，透明度为 0.8 */
  margin-bottom: 10px; /* 添加底部边距 */
  margin-top: 10px;
}
#chatContent .text-right {
  background-color: rgba(204, 238, 219, 0.8);
  margin-right: 5px!important;
  margin-left: auto;
}
#chatContent .text-left {
  background-color: rgba(255,255,255,0.8);
  margin-right: auto;
  margin-left: 5px;
}
.chatBackground {
  width:100%;
  background-image: url('https://th.bing.com/th/id/OIP._bQAqyc05wuTA_ghVPpJHwHaQD?rs=1&pid=ImgDetMain');

}

</style>

<template>
  <!-- 聊天模态框 -->
  <transition name="slide">
    <div
      class="chat-modal"
      v-if="isVisible"
    >
      <div class="modal-content">
        <!-- 模态框头部 -->
        <div class="modal-header">
          <h5 class="modal-title">
            {{ mode }}
          </h5>
          <div class="basic-button">
            <button type="button" class="btn btn-sm me-1 add" @click="startNewConversation">
              <i class="fas fa-edit"></i>
            </button>
            <button type="button" class="close btn p-0" @click="closeModal" aria-label="关闭">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
        </div>
        
        <!-- 模态框主体 -->
        <div class="chat-container" ref="chatContent">
          <div id="chatContent">
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
              <div class="message-text">
                <template v-if="!msg.isOptions">
                  <div v-html="formatMessage(msg.text)"></div>
                </template>
                <template v-else>
                  <div v-html="formatMessage(msg.text)"></div>
                </template>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 预设选项按钮区域 -->
        <transition name="fade">
          <div class="preset-options" v-if="showPresetOptions">
            <button 
              v-for="(option, index) in presetOptions" 
              :key="index"  
              class="preset-option-btn rounded-pill"
              @click="handlePresetOption(option)"
            >
              <i :class="option.icon"></i>
              {{ option.text }}
            </button>
          </div>
        </transition>
        
        <!-- 预设问题按钮区域 -->
        <div class="preset-questions">
          <button 
            v-for="(question, index) in question_list" 
            :key="index" 
            class="preset-button"
            @click="handlePresetQuestion(question)"
          >
            {{ question }}
          </button>
        </div>
        
        <!-- 选项按钮区域（单独呈现） -->
        <div class="option-buttons" v-if="currentOptions.length > 0">
          <button 
            v-for="(option, index) in currentOptions" 
            :key="index" 
            class="option-btn"
            @click="handleUserAnswer(option.key, option.value)"
          >
            {{ option.key }}: {{ option.value }}
          </button>
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
            send
          </button>
        </div>
        
        <!-- 归属信息 -->
        <div class="attribution">
          Icon by <a href="https://www.flaticon.com/free-icon/ai_2814666?term=robot&page=1&position=9&origin=search&related_id=2814666" target="_blank">Flaticon</a>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
/* eslint-disable */
import axios from "axios";
import { ref } from "vue";

const randomClaim = ref('')

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
      type: String,
      default: ''
    },
    mindMapData: {
      type: Object,
      default: null
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
      messages: [],
      user_cookie: '',
      question_list: [],
      presetOptions: [
        { icon: 'fas fa-plus', text: 'Critical exercises' },
        { icon: 'fas fa-search', text: 'Explore Claims' },
      ],
      showPresetOptions: true,
      exercises: [],
      currentExerciseIndex: 0,
      isQuizActive: false,
      currentOptions: [] // 新增：当前选项按钮
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
        this.messages = [{ text: `正在加载关于支持观点" ${newVal} "的理由...`, sender: 'bot' }]
        this.getGptReply(newVal)
        this.getQuestionList(newVal)
      }
    },
    mindMapData(newVal){
      console.log("newVal",newVal)
      if(newVal){
        randomClaim.value = this.choiceRandomClaim()
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
        this.scrollToBottom()
        if(this.claim){
          // 一旦用户发送信息，则取消预设选项
          this.showPresetOptions = false;
          axios.get(`http://localhost:5000/roleplay?claim=${this.claim}&message=${this.message}`,{withCredentials: true})
          .then(response => {
            this.messages.push({text: response.data, sender: 'bot'})
            this.scrollToBottom();
          })
          .catch(error => {
            console.error("return reply error: ", error)
          })
        }else{
          // 正常对话 -- normal conversation
          axios.get(`http://localhost:5000/normal_conversation?message=${this.message}`,{withCredentials: true})
          .then(response => {
            this.messages.push({text: response.data, sender: 'bot'})
            this.scrollToBottom();
          })
          .catch(error => {
            console.error("return reply error: ", error)
          })
        }
        this.message = '';
      }
    },
    startNewConversation(){
      // 清空当前对话
      this.messages = [];
      // 重新显示预设选项
      this.showPresetOptions = true;
      // 重置当前选项
      this.currentOptions = [];
      // 可能需要重置其他相关状态
      // 例如：重置 claim
      this.$emit('reset-claim');
    },
    handlePresetQuestion(question) {
      if (question.trim() !== '') {
        const userMessage = question;
        this.messages.push({ text: userMessage, sender: 'user' });
        this.showPresetOptions = false;
        if(this.claim){
          axios.get(`http://localhost:5000/roleplay?claim=${this.claim}&message=${userMessage}`, { withCredentials: true })
            .then(response => {
              this.messages.push({ text: response.data, sender: 'bot' });
              this.scrollToBottom();
              this.getQuestionList(response.data)
            })
            .catch(error => {
              console.error("返回回复错误: ", error)
            });
        }else{
          // 如果claim为空，则使用随机选择的claim
          axios.get(`http://localhost:5000/roleplay?claim=${randomClaim.value}&message=${userMessage}`, { withCredentials: true })
            .then(response => {
              this.messages.push({ text: response.data, sender: 'bot' });
              this.scrollToBottom();
              this.getQuestionList(response.data)
            })
            .catch(error => {
              console.error("返回回复错误: ", error)
            });
        }
        this.question_list = []
      }
    },
    handlePresetOption(option) {
      console.log('Selected option:', option);
      // 这里可以根据选项执行相应的操作，比如发送特定的消息
      this.message = option.text;
      // 完成特定的操作
      this.messages.push({ text: this.message, sender: 'user' });
      if(option.text === 'Critical exercises'){
        this.messages.push({text: `随机选取claim: ${randomClaim.value}进行Critical Exercises，请回答以下问题：`, sender: 'bot'})
        console.log("randomClaim.value", randomClaim.value)
        axios.get(`http://localhost:5000/critical_thinking?claim=${randomClaim.value}`, {withCredentials: true})
        .then(response => {
          this.exercises = response.data['exercises']
          console.log("exercises", this.exercises)
          this.CriticalExercises()
        })
        .catch(error => {
          console.error("Critical Exercises error", error)
        })
      }
      if(option.text === 'Explore Claims'){
        this.ExploreClaims()
      }
      // this.sendMessage();
      this.showPresetOptions = false; // 隐藏预设选项
      this.message = '';
    },

    handleUserAnswer(selectedKey, selectedValue){
     // 显示用户选择的答案
     console.log("this.currentExerciseIndex", this.currentExerciseIndex)
     this.messages.push({
       text: `你选择了: ${selectedKey}: ${selectedValue}`,
       sender: 'user'
     });
     this.scrollToBottom();

     // 显示正确答案
     const currentExercise = this.exercises[this.currentExerciseIndex]
     const questionData = JSON.parse(currentExercise.choice);
     const currentItem = questionData[this.questionIndex];
     if (currentItem && currentItem.Correct) {
       this.messages.push({
         text: `正确答案是: ${currentItem.Correct} 理由如下: ${currentItem.Explanation}`,
         sender: 'bot'
       });
       this.scrollToBottom();
     }
     // 清空当前选项
     this.currentOptions = [];
     // 增加questionIndex以遍历下一个问题
     this.questionIndex++;
     if (this.questionIndex < questionData.length) {
       setTimeout(() => {
         this.displayCurrentExercise();
       }, 1000); // 可根据需要调整延迟时间
     } else {
       this.scrollToBottom();
       this.isQuizActive = false;
       this.questionIndex = 0;
       this.currentExerciseIndex++;
       if (this.currentExerciseIndex < this.exercises.length) {
         // 如果还有其他练习，可以选择继续
         this.displayCurrentExercise();
       } else {
         // 所有练习完成后的处理
         this.messages.push({
           text: '所有练习已完成。',
           sender: 'bot'
         });
         this.scrollToBottom();
       }
     }
   },

    ExploreClaims(){
      console.log("Explore Claims")
      console.log("claim", randomClaim.value)
      // 将claim作为参数传递给getGptReply
      if(randomClaim.value){  
        this.message = `正在加载关于支持观点" ${randomClaim.value} "的理由...`
        this.messages.push({text: this.message, sender: 'bot'})
        this.getGptReply(randomClaim.value)
        // 准备问题
        this.getQuestionList(randomClaim.value)
      }
    },
    CriticalExercises(){
      console.log("Critical Exercises")
      if(this.exercises.length > 0){
        this.isQuizActive = true
        this.currentExerciseIndex = 0
        this.displayCurrentExercise()
      }
    },
    displayCurrentExercise() {
      const exercise = this.exercises[this.currentExerciseIndex]
      if(exercise){
        let questionData = []
        console.log("exercise", exercise)
        try {
          questionData = JSON.parse(exercise.choice);
          console.log("questionData", questionData)
        } catch (e) {
          console.error("解析问题数据出错:", e);
        }
        // 使用独立的questionIndex来遍历questionData
        if (!this.questionIndex) {
          this.questionIndex = 0;
        }
        const currentItem = questionData[this.questionIndex]
        if (currentItem && currentItem.Statement) {
          this.messages.push({
            text: `Statement ${this.questionIndex + 1}: ${currentItem.Statement}`,
            sender: 'bot'
          });
          this.scrollToBottom();

          if (currentItem.Argument) {
            this.messages.push({
              text: `Argument: ${currentItem.Argument}`,
              sender: 'bot'
            });
            this.scrollToBottom();
          }
          // 设置当前选项
          this.setCurrentOptions(currentItem.options)
        }
      }
    },
    setCurrentOptions(options) {
      // 将选项转换为数组形式
      this.currentOptions = Object.entries(options).map(([key, value]) => ({
        key,
        value
      }));
    },
    getMessageClass(sender) {
      return sender === 'user' ? 'user-message' : 'bot-message';
    },
    getAvatar(sender) {
      return sender === 'user' ? this.userAvatar : this.botAvatar;
    },
    getGptReply(claim){
      this.showPresetOptions = false;
      axios.get(`http://localhost:5000/roleplay?claim=${claim}`,{withCredentials: true})
      .then(response => {
        this.messages.push({text: response.data, sender: 'bot'})
        this.scrollToBottom();
        const userId = this.getCookie('user_id')
        if(userId){
          this.userId = userId
          console.log('获取到的 user_id:', this.userId);
        }
      })
      .catch(error => {
        console.error('roleplay first reply error', error)
      })
    },
    scrollToBottom() {
      this.$nextTick(() => {
       const chatContainer = this.$refs.chatContainer;
       if (chatContainer) {
         chatContainer.scrollTop = chatContainer.scrollHeight;
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
    },
    getCookie(name){
      const value = `; ${document.cookie}`;
      const parts = value.split(`; ${name}=`);
      if (parts.length === 2) return parts.pop().split(';').shift();
      return null;
    },
    getQuestionList(claim){
      axios.get(`http://localhost:5000/roleplay/prompt?claim=${claim}`, {withCredentials: true})
      .then(response => {
        try {
          // 假设 response.data 是一个字符串，需要解析为 JSON
          console.log("response.data",response.data)
          this.question_list = response.data.question_list
        } catch (e) {
          console.error("解析问题列表时出错:", e);
        }
      })
      .catch(error => {
        console.error('roleplay question list error', error)
      })
    },
    choiceRandomClaim() {
      if (!this.mindMapData) {
        console.warn("No data available for choiceRandomClaim");
        return;
      }
      console.log("mindMapData", this.mindMapData);
      const collectNodeTexts = (node) => {
      if (!node) return [];
      let texts = [node.data.text];
      if (node.children && node.children.length > 0) {
          node.children.forEach(child => {
            texts = texts.concat(collectNodeTexts(child));
          })
        }
        return texts;
      };
      const allTexts = collectNodeTexts(this.mindMapData);
      if (allTexts.length === 0) {
          console.warn("No texts found in mindMapData");
          return;
        }

      const randomIndex = Math.floor(Math.random() * allTexts.length);
      const returnText = allTexts[randomIndex];
      console.log("随机选择的文本:", returnText);
      return returnText;
    },
  },
};
</script>

<style scoped>
/* 自定义样式 */

/* 过渡效果 */
.slide-enter-active, .slide-leave-active {
  transition: transform 0.4s ease, opacity 0.4s ease;
}

.slide-enter-from {
  opacity: 0;
}

.slide-enter-to {
  opacity: 1;
}

.slide-leave-from {
  opacity: 1;
}

.slide-leave-to {
  opacity: 0;
}

/* 基础模态框样式 */
.chat-modal {
  background: rgba(255, 255, 255, 0.9); /* 浅色背景 */
  position: fixed; /* 固定位置 */
  bottom: 50px; /* 距离底部20px */
  right: 20px; /* 距离右侧20px */
  width: 540px; /* 设置固定宽度 */
  max-width: 90%; /* 响应式宽度 */
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  border-radius: 10px;
  overflow: hidden;
  z-index: 10000; /* 确保在其他内容之上 */
}

/* 内容区域样式 */
.modal-content {
  background: #f9f9f9; /* 浅色背景 */
  border: none;
  border-radius: 10px;
  overflow: hidden;
}

/* 头部样式 */
.modal-header {
  background: #ffffff; /* 统一的浅色调 */
  color: #333;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 10px;
  border-bottom: 1px solid #ddd;
}

.modal-header .modal-title {
  font-family: 'Roboto', sans-serif;
  font-weight: 500;
}


.modal-header .add {
  font-size: 15px;
  color: #bbb;
  transition: color 0.3s;
  justify-content: flex-end;
}

.modal-header .add:hover {
  color: #333;
}

.modal-header .close {
  font-size: 24px;
  color: #bbb;
  transition: color 0.3s;
  justify-content: flex-end;
}

.modal-header .close:hover {
  color: #333;
}



/* 聊天区域样式 */
.chat-container {
  background: #ffffff;
  padding: 20px;
  height: 320px; /* 调整高度 */
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
  padding: 5px 5px;
  border-radius: 15px;
  background: #e0e0e0;
  color: #333;
  font-family: 'Roboto', sans-serif;
  word-wrap: break-word;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  position: relative;
  white-space: pre-wrap; /* 保留换行符 */
  font-size: 12px;
  text-align: left;
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
  color:#ddd;
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

/* 预设问题按钮样式 */
.preset-questions {
  background: rgba(255, 255, 255, 0.8);
  padding: 10px 20px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.preset-button {
  padding: 8px 16px;
  border: none;
  border-radius: 20px;
  background: #20c997; /* 蓝绿色背景 */
  color: #fff;
  cursor: pointer;
  transition: background 0.3s, transform 0.2s, box-shadow 0.3s;
  font-size: 14px;
}

.preset-button:hover {
  background: #17a2b8; /* 悬停时的蓝绿色 */
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

/* 预设选项的淡入淡出效果 */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
}

/* 预设选项的列表效果 */
.list-enter-active, .list-leave-active {
  transition: all 0.3s;
}

.list-enter, .list-leave-to {
  opacity: 0;
  transform: translateY(30px);
}


/* 响应式调整 */
@media (max-width: 800px) {
  .chat-modal {
    width: 90%; /* 调整宽度 */
    right: 5%; /* 调整右边距 */
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


/* 预设选项按钮样式 */
.preset-options {
  display: flex;
  flex-direction: column;
  padding: 10px;
  background-color: white;
}

.preset-option-btn {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  margin-bottom: 5px;
  border: none;
  background-color: white;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
  text-align: left;
}

.preset-option-btn:hover {
  background-color: #e9e9e9;
}

.preset-option-btn i {
  margin-right: 10px;
  font-size: 16px;
  width: 20px;
  text-align: center;
}

/* 选项按钮样式 */
.option-btn {
  padding: 8px 16px;
  margin: 5px;
  border: none;
  border-radius: 20px;
  background: #20c997; /* 与预设按钮颜色一致 */
  color: #fff;
  cursor: pointer;
  transition: background 0.3s, transform 0.2s;
  font-size: 14px;
}

.option-btn:hover {
  background: #17a2b8;
  transform: translateY(-2px);
}

/* 单独的选项按钮区域样式 */
.option-buttons {
  padding: 10px 20px;
  background: rgba(255, 255, 255, 0.8);
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
</style>
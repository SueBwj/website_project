<template>
  <nav class="navbar">
  <div class="container-fluid">
    <a class="navbar-brand" href="#">Reddit.ai</a>
    </div>
  </nav>
  <div class="container-fluid text-center mt-5">
    <div class="row">
      <div class="col-4 comment-container">
        <CommentReddit 
        :clickContent="currentClickContent"
        :replyComment="replyComment"
        />
      </div>
      <div class="col-8">
        <MindMap 
        @update-click-content="updateClickContent" 
        />
      </div>
    </div>
    <div class="chat-container">
      <button 
        type="button" 
        class="btn btn-light shadow" 
        id="liveToastBtn" 
        @click="toggleChatModal"
      >
        <img src='../assets/ai.png' class="me-2">
        Explore claims
      </button>
      <!-- <div class="toast" role="alert" aria-live="assertive" aria-atomic="true">
        <div class="toast-header">
          <img src="../assets/ai.png" class="rounded me-2" alt="...">
          <strong class="me-auto">Bootstrap</strong>
          <small>11 mins ago</small>
          <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
        <div class="toast-body">
          Hello, world! This is a toast message.
        </div>
      </div> -->
      <div class="chat-modal">
        <ChatModal 
        :visible="isChatModalVisible" 
        @close="isChatModalVisible = false"
        @update-reply-comment="updateReplyComment"
        />
      </div>
    </div>
    
  </div>
</template>

<script>
/* eslint-disable */
import MindMap from '@/components/MindMap.vue';
import CommentReddit from '@/components/CommentReddit.vue';
import ChatModal from '@/components/ChatModal.vue';
import {ref} from 'vue';


export default {
  name: 'HomeView',
  components: {
    MindMap,
    CommentReddit,
    ChatModal
  },
  setup() {
    const isChatModalVisible = ref(false); // 控制对话框的可见性
    const currentClickContent = ref('')
    const replyComment = ref('')
    const toggleChatModal = () => {
      isChatModalVisible.value = !isChatModalVisible.value; // 切换对话框的可见性
    };

    const updateClickContent = (content) => {
      currentClickContent.value = content
    }

    const updateReplyComment = (content) => {
      console.log("HomeView updating replyComment:", content);
      replyComment.value = content;
    }

    return {
      isChatModalVisible,
      toggleChatModal,
      updateClickContent,
      currentClickContent,
      replyComment,
      updateReplyComment
    };
  }
}
</script>

<style>

#liveToastBtn {
  position: fixed; /* 固定位置 */
  bottom: 50px; /* 距离底部20px */
  right: 20px; /* 距离右侧20px */
  z-index: 9999; /* 确保在其他内容之上 */
}

.comment-container {
  max-height: 800px;
  overflow-y: auto; /* 允许垂直滚动 */
}

/* 其他样式保持不变 */
#liveToastBtn {
  position: fixed; /* 固定位置 */
  bottom: 50px; /* 距离底部20px */
  right: 20px; /* 距离右侧20px */
  z-index: 9999; /* 确保在其他内容之上 */
}

</style>
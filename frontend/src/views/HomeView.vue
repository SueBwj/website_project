<template> 
  <nav class="navbar">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">Reddit.ai</a>
    </div>
  </nav>
  <div class="container-fluid text-center mt-5">
    <div class="flex-container">
      <div
        ref="leftPanel"
        class="comment-container"
        :style="{ width: leftWidth + 'px' }"
      >
        <CommentReddit 
          :clickContent="currentClickContent"
          :replyComment="replyComment"
        />
      </div>
      <div
        ref="divider"
        class="divider"
        @mousedown="onMouseDown"
        @touchstart="onTouchStart"
      ></div>
      <div ref="rightPanel" class="mindmap-container">
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
import { ref } from 'vue';

export default {
  name: 'HomeView',
  components: {
    MindMap,
    CommentReddit,
    ChatModal
  },
  setup() {
    const isChatModalVisible = ref(false); // 控制对话框的可见性
    const currentClickContent = ref('');
    const replyComment = ref('');

    const leftWidth = ref(450); // 左侧面板的初始宽度
    const isDragging = ref(false);
    const startX = ref(0);
    const startLeftWidth = ref(0);

    const toggleChatModal = () => {
      isChatModalVisible.value = !isChatModalVisible.value; // 切换对话框的可见性
    };

    const updateClickContent = (content) => {
      currentClickContent.value = content;
    };

    const updateReplyComment = (content) => {
      console.log('HomeView updating replyComment:', content);
      replyComment.value = content;
    };

    const onMouseDown = (e) => {
      isDragging.value = true;
      startX.value = e.clientX;
      startLeftWidth.value = leftWidth.value;
      document.addEventListener('mousemove', onMouseMove);
      document.addEventListener('mouseup', onMouseUp);
    };

    const onMouseMove = (e) => {
      if (!isDragging.value) return;
      const deltaX = e.clientX - startX.value;
      leftWidth.value = startLeftWidth.value + deltaX;
      // 添加最小和最大宽度限制
      if (leftWidth.value < 200) leftWidth.value = 200;
      if (leftWidth.value > window.innerWidth - 200) leftWidth.value = window.innerWidth - 200;
    };

    const onMouseUp = () => {
      isDragging.value = false;
      document.removeEventListener('mousemove', onMouseMove);
      document.removeEventListener('mouseup', onMouseUp);
    };

    const onTouchStart = (e) => {
      if (e.touches.length === 1) {
        onMouseDown(e.touches[0]);
        document.addEventListener('touchmove', onTouchMove);
        document.addEventListener('touchend', onTouchEnd);
      }
    };

    const onTouchMove = (e) => {
      if (e.touches.length === 1) {
        onMouseMove(e.touches[0]);
      }
    };

    const onTouchEnd = () => {
      onMouseUp();
      document.removeEventListener('touchmove', onTouchMove);
      document.removeEventListener('touchend', onTouchEnd);
    };

    return {
      isChatModalVisible,
      toggleChatModal,
      updateClickContent,
      currentClickContent,
      replyComment,
      updateReplyComment,
      leftWidth,
      onMouseDown,
      onTouchStart
    };
  }
}
</script>

<style>
.flex-container {
  display: flex;
  height: calc(100vh - 100px); /* 调整高度，根据需要设置 */
}

.comment-container {
  overflow-y: auto;
}

.divider {
  width: 5px;
  cursor: col-resize;
}

.mindmap-container {
  flex: 1;
  overflow: auto;
}

/* 保持其他样式 */
#liveToastBtn {
  position: fixed; /* 固定位置 */
  bottom: 50px; /* 距离底部50px */
  right: 20px; /* 距离右侧20px */
  z-index: 9999; /* 确保在其他内容之上 */
}
</style>

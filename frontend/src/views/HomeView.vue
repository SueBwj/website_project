<template>
  <div class="container-fluid text-center mt-5">
    <div class="row">
      <div class="col-4">
        <CommentReddit />
      </div>
      <div class="col-8">
        <MindMap />
      </div>
    </div>
    <div class="chat">
      <button type="button" class="btn btn-light" id="liveToastBtn">
      Explore claims
      </button>
      <div class="toast" role="alert" aria-live="assertive" aria-atomic="true">
        <div class="toast-header">
          <img src="../assets/ai.png" class="rounded me-2" alt="...">
          <strong class="me-auto">Bootstrap</strong>
          <small>11 mins ago</small>
          <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
        <div class="toast-body">
          Hello, world! This is a toast message.
        </div>
      </div>
    </div>
    
  </div>
</template>

<script>
/* eslint-disable */
import MindMap from '@/components/MindMap.vue';
import CardVuetify from '@/components/CardVuetify.vue';
import CommentReddit from '@/components/CommentReddit.vue';


export default {
  name: 'HomeView',
  components: {
    MindMap,
    CardVuetify,
    CommentReddit
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

</style>
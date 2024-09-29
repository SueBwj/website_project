<template>
  <div class="container-fluid text-center mt-5">
    <div class="row">
      <div class="col-4">
        <CommentReddit />
      </div>
      <div class="col-8">
        <MindMapView />
      </div>
    </div>
  </div>
</template>

<script>
/* eslint-disable */
import MindMapView from './MindMapView.vue';
import CardVuetify from '@/components/CardVuetify.vue';
import CommentReddit from '@/components/CommentReddit.vue';

export default {
  name: 'HomeView',
  components: {
    MindMapView,
    CardVuetify,
    CommentReddit
  }
}
</script>

<style>
</style>
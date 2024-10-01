<template>
  <div class="topic">
    <h2>Topic</h2>
    <v-card  
        class="mx-auto"
        variant="text"
      >
      <div>
      <v-card-item>
        <template v-slot:prepend>
          <v-avatar
            color="grey-darken-3"
            image="https://avataaars.io/?avatarStyle=Transparent&topType=ShortHairShortCurly&accessoriesType=Prescription02&hairColor=Black&facialHairType=Blank&clotheType=Hoodie&clotheColor=White&eyeType=Default&eyebrowType=DefaultNatural&mouthType=Default&skinColor=Light"
          ></v-avatar>
        </template>
        <v-card-title class="text-left">Nicole</v-card-title>
        <v-card-subtitle class="text-left">Vue Creator</v-card-subtitle>
      </v-card-item>
      <h2 class="text-left pl-4 font-weight-bold" :style="{ fontSize: '25px' }">You should try to start a business with AI Now</h2>
      <v-card-text class="py-1 text-left pl-10" :style="{ fontSize: '20px' }">
        We are in an insane timeline. This is probably as big as the .com boom in my opinion. Maybe bigger.

If you are struggling for cash, are out of a job, or just want to start a side hustle; do it and now!

You have the best tool infront of you. ChatGPT.

With voice mode released, the potential of business ideas have just opened up even further. I sense a lot of children books coming along with natural voices, mini skits, shows, and that sort of thing.

Then you have text to pictures which has been out for a long while but videos are starting to pickup and are only getting better.
      </v-card-text>
    </div>
      
    </v-card>
  </div>
  <div class="comments pt-5">
    <h3 >Comments</h3>
    <div class="row m-2">
      <CardVuetify :comments="comments[0]"/>
    </div>
    <div class="row m-2">
      <CardVuetify :comments="comments[0]" />
    </div>
    <div class="row m-2">
      <CardVuetify :comments="comments[0]" />
    </div>
    <div class="row m-2">
      <CardVuetify :comments="comments[0]" />
    </div>
  </div>
</template>

<script>
/* eslint-disable */
import CardVuetify from './CardVuetify.vue'

export default {
name: 'CommentReddit',
components: {
  CardVuetify
},
data(){
    return{
      comments: [
      {
        author: 'John Doe',
        content: 'This is the first comment.',
        replies: [
          {
            author: 'Jane Doe',
            content: 'I agree with you!',
            replies: [
              {
                author: 'Bob Smith',
                content: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
                replies: []
              }
            ]
          }
        ]
      }
    ],
  }
  
},
}

</script>
<style>
h3{
  text-align: left;
  margin-left: 1em;
 }

</style>
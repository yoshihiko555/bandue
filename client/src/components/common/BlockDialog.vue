<template>
  <v-dialog
    v-model='isBlockedDialog'
    persistent
    max-width='400px'
  >
    <v-card>
      <v-container
        fluid
      >
        <v-row>
          <v-spacer></v-spacer>
          <v-col
            cols='10'
            align=center
          >
            {{ eventDict[event] }}出来ません。
          </v-col>
          <v-btn
            color='teal darken-1'
            class='white--text'
            tile
            depressed
            icon
            @click='closeModal'
          >
            <v-icon>mdi-close-octagon</v-icon>
          </v-btn>
        </v-row>
        <v-row>
          <v-col
            cols='12'
            align=center
          >
          {{ username }}さんにブロックされています。
          </v-col>
        </v-row>
      </v-container>
    </v-card>
  </v-dialog>
</template>
<script>
export default {
  name: 'BlockModel',
  props: ['isBlockedDialog', 'event', 'username'],
  data: () => ({
    eventDict: {
      'follow': 'フォロー',
      'like': 'いいね',
      'retweet': 'リツイート',
      'reply': 'リプライ',
    }
  }),
  methods: {
    closeModal () {
      this.$emit('closeModal')
    }
  }
}
</script>

<template>
    <v-card
        flat
        class='loading_wrap'
    >
        <div class='spacer'></div>
        <vue-loading
            type="cylon"
            color="#aaa"
            :size='{ width: "30px", height: "30px" }'
        ></vue-loading>
    </v-card>
</template>

<script>
    import { VueLoading } from 'vue-loading-template'

    export default {
        name: 'Loading',
        components: {
            VueLoading,
        },
    }
</script>

<style>
    .spacer {
        height: 30px;
    }
</style>

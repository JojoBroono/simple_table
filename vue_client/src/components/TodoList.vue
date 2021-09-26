<template>
    <div>
        <ul>
            <li v-for="item in items" :key="item">{{item}}</li>
        </ul>
    </div>
</template>

<script>
export default {
    props: ['items']
}
</script>  
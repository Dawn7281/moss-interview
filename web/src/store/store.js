// store.js
export default new Vuex.Store({
  state: {
    publishedPosts: []
  },
  mutations: {
    addPost(state, post) {
      state.publishedPosts.unshift(post);
    }
  }
});
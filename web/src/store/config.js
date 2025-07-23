import { defineStore } from 'pinia'

export const useConfigStore = defineStore('config', {
  state: () => ({
    config: {
      enable_knowledge_base: false,
      enable_knowledge_graph: false,
      embed_model: '',
      embed_model_names: {}
    }
  }),
  actions: {
    updateConfig(newConfig) {
      this.config = { ...this.config, ...newConfig }
    }
  }
})
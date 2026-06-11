import { defineStore } from 'pinia'


export const useFormStore = defineStore('formData', {
  state: () => ({
    code: "",
    duration: "",
    is_one_time: false,
  }),
  actions: {
    mutateCode(code: string) {
      this.code = code
    },
    mutateDuration(duration: string) {
      this.duration = duration
    },
    mutateBurnOnReading(bool: boolean) {
      this.is_one_time = bool
    }
  }
})

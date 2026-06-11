import type { ApiCapabilities } from '@/types/ApiTypes'
import { defineStore } from 'pinia'

interface IAppState {
  serviceName: string,
  serviceDescription: string,
  isViewMode: boolean,
  isSideBarVisible: boolean,
  apiCapabilities: ApiCapabilities
  modal: {
    isVisible: boolean,
    content: string,
  },
}
export const useAppStore = defineStore('app', {
  state: (): IAppState => ({
    serviceName: "Javan's Pastebin",
    serviceDescription: "A Public, generic pastebin service",
    isViewMode: false,
    isSideBarVisible: false,
    apiCapabilities: {
      "expiry_durations": []
    },
    modal: {
      isVisible: false,
      content: "",
    }
  }),
  actions: {
    toggleSidebar() {
      this.isSideBarVisible = !this.isSideBarVisible
    },
    toggleViewMode() {
      this.isViewMode = !this.isViewMode
    },
    populateApiCapabilities(caps: ApiCapabilities) {
      this.apiCapabilities = caps;
    },
    toggleModal() {
      this.modal.isVisible = !this.modal.isVisible
    }
  }
})

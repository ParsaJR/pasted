import { useAppStore } from "@/stores/appStore";

export function useModal() {
  function show(content: string) {
        useAppStore().modal.isVisible = true
        useAppStore().modal.content = content
    }

    function toggle() {
        useAppStore().toggleModal()
    }

    return { show, toggle }
}

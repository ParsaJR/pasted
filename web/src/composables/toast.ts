import { toast, type ToastType } from 'vue3-toastify';

export function useToast(body: string, type: ToastType) {
  toast(body,
    {
      isLoading: false,
      position: "bottom-left",
      hideProgressBar: true,
      theme: 'light',
      type: type,

    }
  )
}

export type ApiResponse = {
  shortCode: string,
  content: string,
}
export type ApiError = {
  statusText: string,
  detail: string,
}

export type ApiCapabilities = {
  expiry_durations: {
    code: string,
    name: string,
  }[]
}

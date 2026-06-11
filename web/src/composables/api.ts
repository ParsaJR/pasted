import type { ApiCapabilities, ApiError, ApiResponse } from "@/types/ApiTypes"

export function useAPI() {
  async function getApiCapabilities(): Promise<ApiCapabilities> {
    const url = "/api/management/what-is-available"

    try {
      const response = await fetch(url, {
        method: "GET"
      })

      if (!response.ok) {
        const res = await response.json() as ApiError
        res.statusText = `${response.status} | ${response.statusText}`
        throw res
      }

      const res = await response.json() as ApiCapabilities
      return res
    }

    catch (error) {
      if (isApiError(error)) {
        throw error
      }
      const internalError: ApiError = { detail: "Internal Error", statusText: "Internal Error" }

      throw internalError
    }

  }

  async function postPasted(code: string, duration: string, is_one_time: boolean): Promise<string> {

    const url = `/api/pastes`

    const bodyJson = { "content": code, "expiry_code": duration, "is_one_time": is_one_time}
    try {

      const response = await fetch(url,
        {
          method: "POST",
          body: JSON.stringify(bodyJson),
          headers: {
            "Content-type": "application/json"
          }
        }
      )

      if (!response.ok) {
        const res = await response.json() as ApiError
        res.statusText = `${response.status} | ${response.statusText}`
        throw res
      }


      const res = await response.json()
      return res["shortcode"]
    } catch (error) {
      console.error(error)
      throw error
    }
  }



  async function getPasted(shortcode: string): Promise<ApiResponse> {
    try {
      const url = `/api/pastes/?shortcode=${shortcode}`

      const response = await fetch(url,
        {
          method: "GET",
        }
      )

      // When the statusCode is not in range 200-299
      if (!response.ok) {
        const res = await response.json() as ApiError
        res.statusText = `${response.status} | ${response.statusText}`
        throw res
      }


      const res = await response.json() as ApiResponse

      return res

    } catch (error) {
      if (isApiError(error)) {
        throw error
      }
      const internalError: ApiError = { detail: "Internal Error", statusText: "Internal Error" }

      throw internalError
    }
  }


  function isApiError(error: unknown): error is ApiError {
    return (error as ApiError).detail !== undefined
  }

  return { postPasted, getPasted, getApiCapabilities }
}

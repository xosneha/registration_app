import { createStore } from 'vuex'
import { useToast } from 'vue-toastification'
import axios, { AxiosError, type AxiosResponse } from 'axios'

export type RegisterUserData = {
  first: string
  last: string
  username: string
  email: string
  password: string
}

export type LoginUserData = {
  username: string
  password: string
}

export type TokenResponse = {
  access_token: string
  token_type: 'bearer'
}

type UserBasics = {
  username: string
  first: string
  last: string
  thumbnail: string
}
type UserSession = {
  ip: string
  browser: string
  time: string
  country: string
}
export type UserProfileResponse = {
  user_basics: UserBasics
  user_sessions: UserSession[]
}

export type State = {
  profile: null | UserProfileResponse
}

const toast = useToast()
const BASE_URL = import.meta.env.VITE_API_BASE_URL;

export default createStore<State>({
  state(): State {
    return {
      profile: null
    }
  },
  getters: {
    token: (state: State) => localStorage.getItem('token')
  },
  actions: {
    formError(context: any, msg: string) {
      toast.error(msg)
    },
    httpError(context: any, data: AxiosError) {
      const response = data.response
      if (!response) {
        toast.error('An unexpected error occurred.')
        return
      }
      toast.error(`${response.status}: ${JSON.stringify(data.response?.data)}`)
    },
    async registerUser(context: any, data: RegisterUserData) {
      try {
        const token = await axios.post<any, AxiosResponse<TokenResponse>>(
          `${BASE_URL}/user_register`,
          { user: data }
        )
        context.commit('SET_TOKEN', token.data['access_token'])
      } catch (error) {
        context.dispatch('httpError', error)
        throw error
      }
    },
    async loginUser(context: any, data: LoginUserData) {
      const formData = new FormData()
      formData.append('username', data.username)
      formData.append('password', data.password)
      try {
        const token = await axios.post<any, AxiosResponse<TokenResponse>>(
          `${BASE_URL}/user_login`,
          formData
        )
        context.commit('SET_TOKEN', token.data['access_token'])
      } catch (error) {
        context.dispatch('httpError', error)
        throw error
      }
    },
    async fetchProfile(context: any) {
      const token = context.getters.token
      try {
        const profile = await axios.get<any, AxiosResponse<UserProfileResponse>>(
          `${BASE_URL}/user_profile`,
          { headers: { Authorization: `Bearer ${token}` } }
        )
        context.commit('SET_PROFILE', profile['data'])
      } catch (error) {
        context.dispatch('httpError', error)
        throw error
      }
    }
  },
  mutations: {
    SET_TOKEN(state: State, token: string) {
      localStorage.setItem('token', token)
    },
    SET_PROFILE(state: State, profile: any) {
      state.profile = profile
    }
  }
})

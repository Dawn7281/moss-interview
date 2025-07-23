import http from '../utils/request'

export function addExperience(data) {
    return http.request({
        url: '/api/experience/add',
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
        },
        data
    })
}

export function listExperiences() {
    return http.request({
        url: '/api/experience/list',
        method: 'get',
        headers: {
            'Content-Type': 'application/json',
        }
    })
}

export function getExperience(data) {
    return http.request({
        url: '/api/experience/get',
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
        },
        data
    })
}

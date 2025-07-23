import http from '../utils/request'

export function getJob(data) {
    return http.request({
        url: '/api/job/get-job',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        data
    })
}
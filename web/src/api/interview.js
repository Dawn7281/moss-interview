import http from '../utils/request'

export function postType(data) {
    return http.request({
        url: '/api/interview/type',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        data
    })
}

export function postPressure(data) {
    return http.request({
        url: '/api/interview/level',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        data
    })
}

export function initBot(data) {
    return http.request({
        url: `/api/interview/init-bot`,
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        data
    })
}

export function txtChart(data) {
    return http.request({
        url: `/api/interview/chart`,
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        data
    })
}

export function textAnalyze(data) {
    return http.request({
        url: '/api/interview/text-analyze',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        data
    })
}

export function textReport(username) {
    return http.request({
        url: `/api/interview/text-report/${username}`,
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
}

export function videoChart(formData, username) {
    return http.request({
        url: `/api/interview/video-chart/${username}`,
        method: 'post',
        data: formData,
        // headers: {
        //     'Content-Type': 'multipart/form-data'
        // }
    })
}

export function updateVCN(data) {
    return http.request({
        url: '/api/interview/update-vcn',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        data
    })
}

export function getBase64(data) {
    return http.request({
        url: `/api/interview/get-audio-base64`,
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
        },
        data
    })
}

export function uploadMedia(formData,username) {
    return http.request({
        url: `/api/interview/upload-media/${username}`,
        method: 'post',
        data: formData,
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })
}

export function handleSentiments(username) {
    return http.request({
        url: `/api/interview/handle_sentiments/${username}`,
        method: 'post',
        headers: {
            'Content-Type': 'multipart/form-data'
        },
    })
}

export function endSentiments(username) {
    return http.request({
        url: `/api/interview/end_sentiments/${username}`,
        method: 'post',
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })
}

export function getQA(username) {
    return http.request({
        url: `/api/interview/get-qa/${username}`,
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
        }
    })
}

export function updateQA(data) {
    return http.request({
        url: `/api/interview/update-qa`,
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
        },
        data
    })
}

export function fetchFrame(formData, time, username) {
    return http.request({
        url: `/api/interview/fetch-frame/${time}/${username}`,
        method: 'post',
        data: formData,
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })
}

export function getHistory(username) {
    return http.request({
        url: `/api/interview/get-history/${username}`,
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
        }
    })
}

export function getInterviewCount(data) {
    return http.request({
        url: `/api/interview/get-interview-count`,
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
        },
        data
    })
}

export function getInterviewTopList(data) {
    return http.request({
        url: `/api/interview/get-interview-top-list`,
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
        },
        data
    })
}
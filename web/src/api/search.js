import http from '../utils/request'

export function getSearch(data) {
    return http.request({
        url: '/api/search/get-search',
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
        },
        data
    })
}

export function getGraph(data) {
    return http.request({
        url: '/api/search/get-graph',
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
        },
        data
    })
}

export function updateGraph(data) {
    return http.request({
        url: '/api/search/update-graph',
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
        },
        data
    })
}

export function feedbackGraph(data) {
    return http.request({
        url: '/api/search/feedback-graph',
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
        },
        data
    })
}
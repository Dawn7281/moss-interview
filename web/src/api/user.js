import http from '../utils/request'

export function addUser(data) {
    return http.request({
        url: '/api/user/register',
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
        },
        data
    })
}

export function checkUser(data) {
    return http.request({
        url: '/api/user/login',
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
        },
        data
    })
}

export function reviseRequirement(data) {
    return http.request({
        url: '/api/user/revise-requirement',
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
        },
        data
    })
}

export function getRequirements(username) {
    return http.request({
        url: `/api/user/get-requirement/${username}`,
        method: 'get',
        headers: {
            'Content-Type': 'application/json',
        }
    })
}

export function reviseSkills(data) {
    return http.request({
        url: '/api/user/revise-skills',
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
        },
        data
    })
}

export function getSkills(username) {
    return http.request({
        url: `/api/user/get-skills/${username}`,
        method: 'get',
        headers: {
            'Content-Type': 'application/json',
        }
    })
}

export function editUserInfo(data) {
    return http.request({
        url: '/api/user/edit-user-info',
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
        },
        data
    })
}

export function getUserInfo(username) {
    return http.request({
        url: `/api/user/get-user-info/${username}`,
        method: 'get',
        headers: {
            'Content-Type': 'application/json',
        }
    })
}

export function editJobInfo(data) {
    return http.request({
        url: '/api/user/edit-job-info',
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
        },
        data
    })
}

export function getJobInfo(username) {
    return http.request({
        url: `/api/user/get-job-info/${username}`,
        method: 'get',
        headers: {
            'Content-Type': 'application/json',
        }
    })
}

export function editInterviewInfo(data) {
    return http.request({
        url: '/api/user/edit-interview-info',
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
        },
        data
    })
}

export function getInterviewInfo(username) {
    return http.request({
        url: `/api/user/get-interview-info/${username}`,
        method: 'get',
        headers: {
            'Content-Type': 'application/json',
        }
    })
}

export function getCheckIn(data){
    return http.request({
        url: '/api/user/get-check-in',
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
        },
        data
    })
}

export function updateCheckIn(data) {
    return http.request({
        url: '/api/user/update-check-in',
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
        },
        data
    })
}
import http from "@/utils/request";

export function uploadCertificate(formData) {
    return http.request({
        url: '/api/upload-certificate',
        method: 'post',
        data: formData,
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })
}

export function uploadResume(formData, username) {
    return http.request({
        url: `/api/upload-resume/${username}`,
        method: 'post',
        data: formData,
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })
}

export function getResume(username) {
    return http.request({
        url: `/api/get-resume/${username}`,
        method: 'get',
        responseType: 'blob'
    })
}

export function resumeOptimization(data) {
    return http.request({
        url: `/api/resume-optimization`,
        method: 'post',
        headers: {
            'Content-Type': 'application/json'
        },
        data
    })
}
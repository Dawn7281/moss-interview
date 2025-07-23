import request from '@/utils/request'
import type { AxiosPromise } from 'axios'

interface Report {
  id: string
  // 其他报告字段...
}

export function fetchReportById(reportId: string): AxiosPromise<Report> {
  return request({
    url: `/api/reports/${reportId}`,
    method: 'get'
  })
}
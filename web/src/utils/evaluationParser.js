export function parseEvaluationData(text) {
  const sections = text.split('#### ')
  const result = []
  
  sections.forEach(section => {
    if (!section.trim()) return
    
    const lines = section.split('\n').filter(line => line.trim())
    const titleMatch = lines[0].match(/(.+?)：(\d+)分/)
    if (!titleMatch) return
    
    const title = titleMatch[1]
    const score = parseInt(titleMatch[2])
    
    const brief = lines[1].replace('**简要评语**：', '').trim()
    const example = lines[2].replace('**示例分析**：', '').trim()
    const suggestion = lines[3].replace('**改进建议**：', '').trim()
    const resources = lines[4].replace('**学习资料**：', '').trim()
    
    result.push({
      title,
      score,
      brief,
      example,
      suggestion,
      resources
    })
  })
  
  return result
}
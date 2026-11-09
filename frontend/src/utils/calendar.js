/**
 * Utility to generate and download RFC 5545 .ics iCalendar files.
 * Works seamlessly across Apple Calendar, Google Calendar, Outlook, and Android calendar apps.
 */

function formatIcsDate(dateObj) {
  const pad = (n) => (n < 10 ? '0' + n : n)
  const y = dateObj.getFullYear()
  const m = pad(dateObj.getMonth() + 1)
  const d = pad(dateObj.getDate())
  const hr = pad(dateObj.getHours())
  const min = pad(dateObj.getMinutes())
  const sec = pad(dateObj.getSeconds())
  return `${y}${m}${d}T${hr}${min}${sec}`
}

function escapeIcsText(str) {
  if (!str) return ''
  return str
    .replace(/\\/g, '\\\\')
    .replace(/;/g, '\\;')
    .replace(/,/g, '\\,')
    .replace(/\n/g, '\\n')
}

/**
 * Generates an .ics file from a PulseItem and initiates download.
 * @param {Object} item - The intelligence item (PulseItem)
 */
export function exportToCalendar(item) {
  if (!item) return false

  const now = new Date()
  let startDate
  let endDate

  if (item.deadline) {
    endDate = new Date(item.deadline)
    // If deadline is invalid, fallback
    if (isNaN(endDate.getTime())) {
      endDate = new Date(now.getTime() + 7 * 24 * 3600 * 1000)
    }
    // Set start time to 1 hour before deadline (or duration of event)
    startDate = new Date(endDate.getTime() - 60 * 60 * 1000)
  } else {
    // If no hard deadline, set an all-day or standard reminder event 3 days later
    startDate = new Date(now.getTime() + 3 * 24 * 3600 * 1000)
    startDate.setHours(9, 0, 0, 0)
    endDate = new Date(startDate.getTime() + 2 * 60 * 60 * 1000)
  }

  const prefix = item.category === 'competition' ? '【工大竞赛截止】' : '【工大学术日程】'
  const summary = escapeIcsText(`${prefix}${item.title}`)
  const location = escapeIcsText(item.location || `${item.campus || '全校'} · ${item.source_site || '合肥工业大学'}`)
  
  const descParts = [
    `【系统提示】HFUT-PerceptPulse 校园情报日程提醒`,
    `项目名称：${item.title}`,
    `归属学院：${item.source_site || '合肥工业大学'}`,
    `适用校区：${item.campus || '全部校区'}`,
    item.location ? `活动地点：${item.location}` : '',
    item.summary ? `情报摘要：${item.summary}` : '',
    item.url ? `校园网原文：${item.url}` : ''
  ].filter(Boolean)

  const description = escapeIcsText(descParts.join('\n'))
  const uid = `pulse-${item.id}-${Date.now()}@hfut.edu.cn`

  const icsLines = [
    'BEGIN:VCALENDAR',
    'VERSION:2.0',
    'PRODID:-//HFUT//PerceptPulse Intelligence//CN',
    'CALSCALE:GREGORIAN',
    'METHOD:PUBLISH',
    'BEGIN:VEVENT',
    `UID:${uid}`,
    `DTSTAMP:${formatIcsDate(now)}`,
    `DTSTART:${formatIcsDate(startDate)}`,
    `DTEND:${formatIcsDate(endDate)}`,
    `SUMMARY:${summary}`,
    `DESCRIPTION:${description}`,
    `LOCATION:${location}`,
    item.url ? `URL:${item.url}` : '',
    // Alarm 1: 1 day before
    'BEGIN:VALARM',
    'ACTION:DISPLAY',
    'DESCRIPTION:HFUT-PerceptPulse 截止提醒：明天即将截止！',
    'TRIGGER:-P1D',
    'END:VALARM',
    // Alarm 2: 2 hours before
    'BEGIN:VALARM',
    'ACTION:DISPLAY',
    'DESCRIPTION:HFUT-PerceptPulse 紧急提醒：距离截止仅剩 2 小时！',
    'TRIGGER:-PT2H',
    'END:VALARM',
    'END:VEVENT',
    'END:VCALENDAR'
  ].filter(Boolean)

  const icsContent = icsLines.join('\r\n')
  const blob = new Blob([icsContent], { type: 'text/calendar;charset=utf-8' })
  const downloadUrl = URL.createObjectURL(blob)

  // Sanitize filename
  const safeFilename = (item.title || 'event')
    .slice(0, 30)
    .replace(/[\\/:*?"<>|]/g, '_')

  const link = document.createElement('a')
  link.href = downloadUrl
  link.setAttribute('download', `${safeFilename}.ics`)
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(downloadUrl)

  return true
}

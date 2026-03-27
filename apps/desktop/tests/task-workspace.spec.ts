import { afterEach, describe, expect, it, vi } from 'vitest'
import { flushPromises, mount } from '@vue/test-utils'

import TaskWorkspacePage from '../src/pages/TaskWorkspacePage.vue'

afterEach(() => {
  vi.unstubAllGlobals()
})

describe('TaskWorkspacePage', () => {
  it('submits title, prompt, and text source to the API', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: vi.fn().mockResolvedValue({ id: 'task-1' }),
    })
    vi.stubGlobal('fetch', fetchMock)

    const wrapper = mount(TaskWorkspacePage)

    await wrapper.get('[aria-label="任务标题"]').setValue('Write market overview')
    await wrapper.get('[aria-label="任务目标"]').setValue('Research AI browser agents and write an article.')
    await wrapper.get('[aria-label="文本资料标题"]').setValue('brief')
    await wrapper.get('[aria-label="文本资料内容"]').setValue('Focus on 2026 products.')
    await wrapper.get('button[type="button"]').trigger('click')
    await wrapper.get('form').trigger('submit')

    expect(fetchMock).toHaveBeenCalledTimes(1)
    const [url, options] = fetchMock.mock.calls[0]
    expect(String(url)).toContain('/api/tasks')
    expect(options.method).toBe('POST')
    expect(JSON.parse(String(options.body))).toEqual({
      title: 'Write market overview',
      user_prompt: 'Research AI browser agents and write an article.',
      sources: [
        {
          source_type: 'text',
          title: 'brief',
          content: 'Focus on 2026 products.',
        },
      ],
    })
  })

  it('does not submit when required title or prompt is empty', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: vi.fn().mockResolvedValue({ id: 'task-1' }),
    })
    vi.stubGlobal('fetch', fetchMock)

    const wrapper = mount(TaskWorkspacePage)

    await wrapper.get('[aria-label="任务标题"]').setValue('')
    await wrapper.get('[aria-label="任务目标"]').setValue('   ')
    await wrapper.get('form').trigger('submit')

    expect(fetchMock).not.toHaveBeenCalled()
  })

  it('rejects empty text source and clears source inputs after successful add', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: vi.fn().mockResolvedValue({ id: 'task-1' }),
    })
    vi.stubGlobal('fetch', fetchMock)

    const wrapper = mount(TaskWorkspacePage)

    await wrapper.get('[aria-label="文本资料标题"]').setValue('   ')
    await wrapper.get('[aria-label="文本资料内容"]').setValue('   ')
    await wrapper.get('button[type="button"]').trigger('click')

    await wrapper.get('[aria-label="任务标题"]').setValue('Task')
    await wrapper.get('[aria-label="任务目标"]').setValue('Prompt')
    await wrapper.get('form').trigger('submit')

    expect(JSON.parse(String(fetchMock.mock.calls[0][1].body)).sources).toEqual([])

    await wrapper.get('[aria-label="文本资料标题"]').setValue('source title')
    await wrapper.get('[aria-label="文本资料内容"]').setValue('source body')
    await wrapper.get('button[type="button"]').trigger('click')

    expect((wrapper.get('[aria-label="文本资料标题"]').element as HTMLInputElement).value).toBe('')
    expect((wrapper.get('[aria-label="文本资料内容"]').element as HTMLTextAreaElement).value).toBe('')
  })

  it('shows a simple submit error when API submission fails', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: false,
      status: 500,
      statusText: 'Internal Server Error',
      json: vi.fn(),
    })
    vi.stubGlobal('fetch', fetchMock)

    const wrapper = mount(TaskWorkspacePage)

    await wrapper.get('[aria-label="任务标题"]').setValue('Task')
    await wrapper.get('[aria-label="任务目标"]').setValue('Prompt')
    await wrapper.get('form').trigger('submit')
    await flushPromises()

    expect(wrapper.text()).toContain('任务提交失败，请稍后重试。')
  })
})

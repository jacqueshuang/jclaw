import { afterEach, describe, expect, it, vi } from 'vitest'
import { flushPromises, mount } from '@vue/test-utils'

import * as api from '../src/lib/api'
import TaskWorkspacePage from '../src/pages/TaskWorkspacePage.vue'

vi.mock('../src/lib/api', async () => {
  const actual = await vi.importActual<typeof import('../src/lib/api')>('../src/lib/api')

  return {
    ...actual,
    getTask: vi.fn().mockResolvedValue(null),
  }
})

afterEach(() => {
  vi.unstubAllGlobals()
  vi.mocked(api.getTask).mockReset()
  vi.mocked(api.getTask).mockResolvedValue(null)
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

  it('shows detail loading state while fetching task detail', async () => {
    vi.mocked(api.getTask).mockImplementation(() => new Promise(() => {}))

    const wrapper = mount(TaskWorkspacePage)
    await flushPromises()

    expect(wrapper.text()).toContain('任务详情加载中...')
  })

  it('shows detail error when fetching task detail fails', async () => {
    vi.mocked(api.getTask).mockRejectedValue(new Error('network'))

    const wrapper = mount(TaskWorkspacePage)

    await flushPromises()

    expect(wrapper.text()).toContain('任务详情加载失败，请稍后重试。')
  })

  it('renders delivered task panels', async () => {
    vi.mocked(api.getTask).mockResolvedValue({
      status: 'delivered',
      knowledge_pack: { summary: 'Research summary', outline: '- intro' },
      deliverable: { content_markdown: '# Draft', content_type: 'article' },
    })

    const wrapper = mount(TaskWorkspacePage)

    await flushPromises()

    expect(api.getTask).toHaveBeenCalledWith('latest')
    expect(wrapper.text()).toContain('Research summary')
    expect(wrapper.text()).toContain('# Draft')
  })
})

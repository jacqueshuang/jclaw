import { describe, expect, it } from 'vitest'
import { mount } from '@vue/test-utils'

import TaskWorkspacePage from '../src/pages/TaskWorkspacePage.vue'

describe('TaskWorkspacePage', () => {
  it('submits title, prompt, and text source', async () => {
    const wrapper = mount(TaskWorkspacePage)

    await wrapper.get('[aria-label="任务标题"]').setValue('Write market overview')
    await wrapper.get('[aria-label="任务目标"]').setValue('Research AI browser agents and write an article.')
    await wrapper.get('[aria-label="文本资料标题"]').setValue('brief')
    await wrapper.get('[aria-label="文本资料内容"]').setValue('Focus on 2026 products.')

    expect(wrapper.text()).toContain('提交任务')
  })
})

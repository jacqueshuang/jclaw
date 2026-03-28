import { afterEach, describe, expect, it, vi } from 'vitest'

import { createTask } from '../src/lib/api'

afterEach(() => {
  vi.unstubAllGlobals()
})

describe('createTask', () => {
  it('throws an explicit error on non-OK responses', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: false,
      status: 500,
      statusText: 'Internal Server Error',
      json: vi.fn(),
    })

    vi.stubGlobal('fetch', fetchMock)

    await expect(createTask({ title: 'demo' })).rejects.toThrow('500')
  })
})

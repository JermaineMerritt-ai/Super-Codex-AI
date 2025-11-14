/**
 * Example test file for Wallaby.js demonstration
 */

describe('Wallaby.js Setup', () => {
  it('should run tests successfully', () => {
    expect(true).toBe(true);
  });

  it('should handle basic arithmetic', () => {
    const add = (a: number, b: number): number => a + b;
    expect(add(2, 3)).toBe(5);
  });

  it('should handle async operations', async () => {
    const asyncAdd = async (a: number, b: number): Promise<number> => {
      return new Promise((resolve) => {
        setTimeout(() => resolve(a + b), 10);
      });
    };

    const result = await asyncAdd(5, 7);
    expect(result).toBe(12);
  });
});
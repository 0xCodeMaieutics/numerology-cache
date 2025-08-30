const CELEBRITIES_KEY = "celebrities";
const CELEBRITIES_INDEX_KEY = `celebId_index`;
const ALL_KEY = `all`;

export const redisKey = {
  celebrities: (celebId: string | null) => ({
    all: `${CELEBRITIES_KEY}:${ALL_KEY}`,
    celebIdIndex: `${CELEBRITIES_KEY}:${celebId}:${CELEBRITIES_INDEX_KEY}`,
    category: (category: string) => `${CELEBRITIES_KEY}:${category}`,
  }),
};

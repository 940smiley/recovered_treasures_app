from typing import List, Dict

def get_stub_comps(query: str) -> List[Dict]:
    return [{"title": f"{query} comparable #{i}", "price": round(19.99 + i,2), "sold": i % 2 == 0} for i in range(1,6)]

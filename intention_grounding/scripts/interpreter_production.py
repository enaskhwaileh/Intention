#!/usr/bin/env python3
"""AB-M1 entry point. Legacy label/confidence generation has been retired.

Call interpret_query with an explicit provider. Results are execution envelopes and
must not be passed into grounder_production. For offline use see interpreter.demo.
"""
from intention_grounding.interpreter.core import interpret


def interpret_query(query, *, input_id, provider):
    return interpret(input_id, query, provider)


def interpret_queries_batch(queries, *, provider):
    return {'results': [interpret_query(query, input_id=f'query-{index}', provider=provider)
                        for index, query in enumerate(queries, 1)]}


if __name__ == '__main__':
    from intention_grounding.interpreter.demo import main
    raise SystemExit(main())

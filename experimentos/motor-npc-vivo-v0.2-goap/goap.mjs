function isRecord(value) {
  return !!value && typeof value === 'object' && !Array.isArray(value) &&
    (Object.getPrototypeOf(value) === Object.prototype || Object.getPrototypeOf(value) === null);
}

function primitive(value) {
  return value === null || ['boolean','string','number'].includes(typeof value);
}

export function validateFacts(facts, label='facts') {
  const errors=[];
  if (!isRecord(facts)) return [label+' debe ser un objeto plano'];
  for (const [key,value] of Object.entries(facts)) {
    if (!key) errors.push(label+': clave vacía');
    if (!primitive(value)) errors.push(label+'.'+key+' debe ser primitivo');
    if (typeof value === 'number' && !Number.isFinite(value)) errors.push(label+'.'+key+' debe ser finito');
  }
  return errors;
}

export function factsMatch(state, conditions) {
  return Object.entries(conditions).every(([key,value]) => Object.hasOwn(state,key) && Object.is(state[key],value));
}

export function applyEffects(state, effects) {
  return { ...state, ...effects };
}

export function validateAction(action) {
  const errors=[];
  if (!isRecord(action)) return ['acción inválida'];
  if (typeof action.id !== 'string' || !action.id.trim()) errors.push('action.id inválido');
  if (!Number.isFinite(action.cost) || action.cost <= 0) errors.push('action.cost debe ser > 0 y finito');
  errors.push(...validateFacts(action.preconditions,'preconditions'));
  errors.push(...validateFacts(action.effects,'effects'));
  return errors;
}

function stateKey(state) {
  return JSON.stringify(Object.keys(state).sort().map(k => [k,state[k]]));
}

function planKey(plan) {
  return plan.join('>');
}

function compareNodes(a,b) {
  if (a.cost !== b.cost) return a.cost-b.cost;
  if (a.plan.length !== b.plan.length) return a.plan.length-b.plan.length;
  return planKey(a.plan).localeCompare(planKey(b.plan));
}

export function planGOAP(initialState, goal, actions, options={}) {
  const maxExpansions=Number.isInteger(options.maxExpansions) ? options.maxExpansions : 5000;
  const stateErrors=validateFacts(initialState,'initialState');
  const goalErrors=validateFacts(goal,'goal');
  if (stateErrors.length || goalErrors.length) {
    throw new TypeError([...stateErrors,...goalErrors].join(' · '));
  }
  if (!Array.isArray(actions) || !actions.length) throw new TypeError('actions debe ser un array no vacío');

  const ids=new Set();
  for (const action of actions) {
    const errors=validateAction(action);
    if (errors.length) throw new TypeError('Acción inválida: '+errors.join(' · '));
    if (ids.has(action.id)) throw new TypeError('action.id duplicado: '+action.id);
    ids.add(action.id);
  }

  const ordered=[...actions].sort((a,b)=>a.id.localeCompare(b.id));
  if (factsMatch(initialState,goal)) {
    return { status:'PLAN_FOUND', plan:[], cost:0, expansions:0, finalState:{...initialState} };
  }

  const queue=[{state:{...initialState},cost:0,plan:[]}];
  const best=new Map([[stateKey(initialState),0]]);
  let expansions=0;

  while (queue.length) {
    queue.sort(compareNodes);
    const node=queue.shift();
    const key=stateKey(node.state);
    if (node.cost !== best.get(key)) continue;
    if (++expansions > maxExpansions) {
      return { status:'SEARCH_LIMIT', plan:null, cost:null, expansions, finalState:null };
    }

    for (const action of ordered) {
      if (!factsMatch(node.state,action.preconditions)) continue;
      const next=applyEffects(node.state,action.effects);
      const cost=node.cost+action.cost;
      const plan=[...node.plan,action.id];

      if (factsMatch(next,goal)) {
        return { status:'PLAN_FOUND', plan, cost, expansions, finalState:next };
      }

      const nextKey=stateKey(next);
      const old=best.get(nextKey);
      if (old === undefined || cost < old) {
        best.set(nextKey,cost);
        queue.push({state:next,cost,plan});
      } else if (cost === old) {
        queue.push({state:next,cost,plan});
      }
    }
  }

  return { status:'NO_PLAN', plan:null, cost:null, expansions, finalState:null };
}

import {LEGACY_DAYS} from './legacy-v1.js';
import {DEFAULT_STATE} from './data.js';
// Three-way merge: retain user edits, deletions, notes and completion states.
// Only default fields that the user never changed follow the new itinerary.
export function migrate(saved){
 if((saved.contentRevision||1)>=2)return saved;
 const next=JSON.parse(JSON.stringify(saved));
 for(const [date,oldItems] of Object.entries(LEGACY_DAYS)){
  const latest=DEFAULT_STATE.days[date];
  next.days[date]=next.days[date].flatMap(item=>{
   const old=oldItems.find(v=>v.id===item.id),fresh=latest.find(v=>v.id===item.id);
   if(!old)return [item];
   if(!fresh)return Object.keys(old).filter(k=>k!=='done').every(k=>item[k]===old[k])?[]:[item];
   return [{...Object.fromEntries(Object.entries(fresh).map(([key,value])=>[key,key==='done'||item[key]!==old[key]?item[key]:value]))}];
  });
  for(const item of latest)if(!oldItems.some(v=>v.id===item.id)&&!next.days[date].some(v=>v.id===item.id))next.days[date].push(JSON.parse(JSON.stringify(item)));
 }
 next.contentRevision=2;
 return next;
}

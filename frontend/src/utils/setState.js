"use client";
export default function SetState(state, prop, updateState, value) {
  updateState({ ...state, [prop]: value });
}

# Story 2.2: Per-Round Message Inboxes

**Epic:** Epic 2
**Week:** Weeks TBD

## User Story

As a protocol node,
I want separate message inboxes per round,
So that messages for round r are isolated from round r+1 (round firewall)..

## Acceptance Criteria

1. Extend `RoundScheduler` with per-round inbox storage: `Dict[int, List[Message]]`
2. `deliver_message(message: Message)` method routing messages to correct round inbox
3. `get_round_messages(round: int) -> List[Message]` method retrieving messages for specific round
4. Messages delivered to `round_inboxes[message.round]`
5. Round firewall: messages for round < current_round logged but not processed for state mutation
6. Late message handling: flag messages arriving after round transition with `post_round=True` metadata
7. Unit tests covering: message routing, inbox isolation, late message handling
8. Integration test: messages delivered across multiple rounds stay isolated

## Prerequisites

Stories 1.9, 2.1

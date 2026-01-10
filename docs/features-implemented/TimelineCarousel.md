# Timeline Carousel

## Overview

Posts in TimelineRiverRow are presented as interactive card decks navigable with arrows or dots.

## Location

`frontend/src/components/pages/Home/components/TimelineRiverRow/`

## Navigation

```jsx
const [currentCard, setCurrentCard] = useState(0);

const nextCard = () => setCurrentCard((prev) => (prev + 1) % totalCards);
const prevCard = () => setCurrentCard((prev) => (prev - 1 + totalCards) % totalCards);
```

## UI Elements

```jsx
<button className="deck-nav deck-prev" onClick={prevCard}>‹</button>
<div className="deck-card">{/* Current post */}</div>
<button className="deck-nav deck-next" onClick={nextCard}>›</button>

<div className="deck-indicators">
  {posts.map((_, index) => (
    <span 
      className={`dot ${index === currentCard ? 'active' : ''}`}
      onClick={() => setCurrentCard(index)}
    />
  ))}
</div>
```

## Visual Design

- Cards appear stacked with subtle offset (shadow card behind)
- Active indicator dot glows cyan
- Navigation arrows glow on hover

## Time Batching

Posts can be grouped into time windows (same day, 3-day windows, weekly).

```jsx
const groupPostsByTimeWindow = (posts, windowDays = 3) => {
  // Group posts that fall within windowDays of each other
};
```

## Keyboard Navigation

- **ArrowLeft** - Previous card
- **ArrowRight** - Next card

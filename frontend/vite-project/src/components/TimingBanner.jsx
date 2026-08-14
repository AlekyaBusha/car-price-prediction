function TimingBanner({ advice }) {
  if (!advice) return null

  const titleMap = {
    wait: "Consider Waiting",
    buy_now: "Good Time to Buy",
    neutral: "Neutral"
  }

  return (
    <div className={`advice-box advice-${advice.recommendation}`}>
      <strong>{titleMap[advice.recommendation]}</strong>
      <p>{advice.message}</p>
    </div>
  )
}

export default TimingBanner
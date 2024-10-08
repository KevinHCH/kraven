document.addEventListener("DOMContentLoaded", function () {
  // limit to 20 cards in the ui
  function monitorCards({ maxCards } = { maxCards: 20 }) {
    const cards = [...document.querySelectorAll("#job-container > div")]
    if (cards.length >= maxCards) {
      cards.slice(maxCards).forEach((card) => card.remove())
    }
  }

  // Create a new EventSource to connect to the stream
  const eventSource = new EventSource("/stream")

  // Listen for new job data from the SSE stream
  eventSource.onmessage = function (event) {
    const jobs = JSON.parse(event.data)

    const jobContainer = document.getElementById("job-container")

    jobs.forEach(function (job) {
      const exist = document.querySelector(`[data-id='${job.id}']`)
      if (exist) {
        return
      }
      // Create a new job card with the job data
      const jobCard = `
                        <div data-id="${
                          job.id
                        }" class="job-card bg-gray-800 border border-slate-600 rounded hover:bg-gray-700 transition-colors p-2">
                            <a href="${job.url}" target="_blank" class="">
                                <h3 class="text-xl font-semibold text-blue-400">${
                                  job.title
                                }</h3>
                            </a>
                            <p class="text-green-400 font-bold mb-2">${
                              job.price ? job.price : job.job_type
                            }</p>
                            <p class="text-gray-300 text-sm">
                                experience: <span class="font-bold">${
                                  job.experience_level
                                }</span>
                            </p>
                            <p class="text-gray-300 text-sm">
                                posted:
                                <span class="font-bold text-green-500">${
                                  job.posted_at
                                }</span>
                            </p>
                            <p class="text-gray-300 text-sm pt-2">${job.description.substring(
                              0,
                              200
                            )}...</p>
                        </div>
                    `
      monitorCards()
      // Insert the new job card at the beginning of the container
      jobContainer.insertAdjacentHTML("afterbegin", jobCard)
    })
  }

  eventSource.onerror = function (error) {
    console.error("EventSource failed: ", error)
  }
})

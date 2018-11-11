import Dates

import CSV
import Pandas
import PyCall

@PyCall.pyimport pandas
@PyCall.pyimport numpy

mutable struct Limit
    TimeStamp::Dates.Date
    Price::Float64
    Size::Float64

    PreviousLimit::Union{Limit, Nothing}
    NextLimit::Union{Limit, Nothing}
end 

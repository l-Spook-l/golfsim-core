# Try to use the real FlightScope parser, fall back to stub if unavailable
try:
    from .parser_flightscope_real import ParserFlightscope
except ImportError:
    from .parser_flightscope_stub import ParserFlightscope

import TimelineItem from "@mui/lab/TimelineItem";
import TimelineSeparator from "@mui/lab/TimelineSeparator";
import TimelineConnector from "@mui/lab/TimelineConnector";
import TimelineContent from "@mui/lab/TimelineContent";
import TimelineDot from "@mui/lab/TimelineDot";
import TimelineOppositeContent from "@mui/lab/TimelineOppositeContent";
import { Avatar, Typography } from "@mui/material";
import riftIcon from "../images/riftIcon.png";

export default function TimelineRift({ heartrate, time }) {
	return (
		<TimelineItem>
			<TimelineOppositeContent
				sx={{ m: "auto 0" }}
				align="right"
				variant="body2"
				color="text.secondary"
			>
				<Typography variant="body1">{heartrate} bpm</Typography>
				<Typography variant="body2">{time}</Typography>
			</TimelineOppositeContent>
			<TimelineSeparator>
				<TimelineConnector />
				<TimelineDot>
					<Avatar alt="Rift" src={riftIcon} />
				</TimelineDot>
				<TimelineConnector />
			</TimelineSeparator>
			<TimelineContent sx={{ py: "30px", px: 4 }}>
				<Typography variant="h6" component="span">
					Rift Herald
				</Typography>
			</TimelineContent>
		</TimelineItem>
	);
}
